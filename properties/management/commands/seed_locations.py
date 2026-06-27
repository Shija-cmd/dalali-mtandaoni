import csv
import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from properties.models import District, Region, StreetArea, Ward


class Command(BaseCommand):

    help = 'Populate Tanzania regions, districts, wards, and street/area data.'

    def add_arguments(self, parser):

        parser.add_argument(
            '--path',
            default=None,
            help='Optional path to a Tanzania locations JSON or CSV file.'
        )

    def handle(self, *args, **options):

        data_path = self._get_data_path(
            options.get('path')
        )

        if not data_path.exists():

            raise CommandError(
                f'Location data file not found: {data_path}'
            )

        data = self._load_data(
            data_path
        )

        is_nested_data = self._is_nested_data(
            data
        )

        imported_counts = {
            'regions': 0,
            'districts': 0,
            'wards': 0,
            'streets': 0,
        }

        with transaction.atomic():

            if is_nested_data:

                self._import_nested_data(
                    data,
                    imported_counts
                )

            else:

                self._import_flat_data(
                    data,
                    imported_counts
                )

        self._print_missing_ward_report()
        self.stdout.write('')
        self.stdout.write(
            f'Regions: {Region.objects.count()}'
        )
        self.stdout.write(
            f'Districts: {District.objects.count()}'
        )
        self.stdout.write(
            f'Wards: {Ward.objects.count()}'
        )
        self.stdout.write(
            f'Streets: {StreetArea.objects.count()}'
        )
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                'Location database populated successfully.'
            )
        )

    def _load_data(self, data_path):

        suffix = data_path.suffix.lower()

        if suffix == '.json':

            with data_path.open(
                encoding='utf-8-sig'
            ) as data_file:

                data = json.load(
                    data_file
                )

        elif suffix == '.csv':

            with data_path.open(
                encoding='utf-8-sig',
                newline=''
            ) as data_file:

                data = list(
                    self._normalize_row_keys(
                        row
                    )
                    for row in csv.DictReader(data_file)
                )

        else:

            raise CommandError(
                'Location data file must be JSON or CSV.'
            )

        if not isinstance(data, list):

            raise CommandError(
                'Location data must be a list of location records.'
            )

        return data

    def _normalize_row_keys(self, row):

        return {
            self._text(key).lower(): value
            for key, value in row.items()
            if key is not None
        }

    def _is_nested_data(self, data):

        return bool(
            data
            and isinstance(data[0], dict)
            and 'districts' in data[0]
        )

    def _import_nested_data(self, data, imported_counts):

        for region_data in data:

            region_name = self._required_text(
                region_data,
                'region',
                'Region'
            )

            region = self._get_region(
                region_name,
                imported_counts
            )

            for district_data in region_data.get('districts', []):

                district_name = self._required_text(
                    district_data,
                    'name',
                    f'District in {region_name}'
                )

                district = self._get_district(
                    region,
                    district_name,
                    imported_counts
                )

                for ward_data in district_data.get('wards', []):

                    ward_name = self._required_text(
                        ward_data,
                        'name',
                        f'Ward in {district_name}'
                    )

                    ward = self._get_ward(
                        district,
                        ward_name,
                        imported_counts
                    )

                    for street_name in ward_data.get('streets', []):

                        street_name = str(street_name).strip()

                        if street_name:

                            self._get_street(
                                ward,
                                street_name,
                                imported_counts
                            )

    def _import_flat_data(self, data, imported_counts):

        for row_number, row in enumerate(data, start=1):

            region_name = self._required_text(
                row,
                'region',
                f'Region in row {row_number}'
            )
            district_name = self._flat_district_name(
                row,
                row_number
            )
            ward_name = self._required_text(
                row,
                'ward',
                f'Ward in row {row_number}'
            )
            street_name = self._text(
                row.get(
                    'street',
                    ''
                )
            )

            region = self._get_region(
                region_name,
                imported_counts
            )
            district = self._get_district(
                region,
                district_name,
                imported_counts
            )
            ward = self._get_ward(
                district,
                ward_name,
                imported_counts
            )

            if street_name:

                self._get_street(
                    ward,
                    street_name,
                    imported_counts
                )

    def _get_region(self, region_name, imported_counts):

        self.stdout.write(
            f'Creating Region: {region_name}'
        )

        region, created = Region.objects.get_or_create(
            name=region_name
        )

        if created:

            imported_counts['regions'] += 1

        return region

    def _get_district(self, region, district_name, imported_counts):

        self.stdout.write(
            f'Creating District: {district_name}'
        )

        district, created = District.objects.get_or_create(
            region=region,
            name=district_name
        )

        if created:

            imported_counts['districts'] += 1

        return district

    def _get_ward(self, district, ward_name, imported_counts):

        self.stdout.write(
            f'Creating Ward: {ward_name}'
        )

        ward, created = Ward.objects.get_or_create(
            district=district,
            name=ward_name
        )

        if created:

            imported_counts['wards'] += 1

        return ward

    def _get_street(self, ward, street_name, imported_counts):

        self.stdout.write(
            f'Creating Street: {street_name}'
        )

        street, created = StreetArea.objects.get_or_create(
            ward=ward,
            name=street_name
        )

        if created:

            imported_counts['streets'] += 1

        return street

    def _flat_district_name(self, row, row_number):

        district_name = (
            self._text(
                row.get(
                    'municipality',
                    ''
                )
            )
            or self._text(
                row.get(
                    'district',
                    ''
                )
            )
        )

        if not district_name:

            raise CommandError(
                f'District in row {row_number} is missing district or municipality.'
            )

        if district_name.endswith(' Municipality'):

            district_name = (
                district_name[:-len(' Municipality')]
                + ' Municipal'
            )

        return district_name

    def _print_missing_ward_report(self):

        missing_districts = District.objects.filter(
            wards__isnull=True
        ).select_related(
            'region'
        ).distinct().order_by(
            'region__name',
            'name'
        )
        missing_count = missing_districts.count()

        if not missing_count:

            return

        self.stdout.write('')
        self.stdout.write(
            self.style.WARNING(
                f'Warning: {missing_count} districts still have no ward records.'
            )
        )
        self.stdout.write(
            'Add an official ward/street CSV or JSON for those districts and run seed_locations --path again.'
        )

        for district in missing_districts[:20]:

            self.stdout.write(
                f'- {district.name}, {district.region.name}'
            )

        if missing_count > 20:

            self.stdout.write(
                f'... and {missing_count - 20} more.'
            )

    def _get_data_path(self, custom_path):

        if custom_path:

            return Path(
                custom_path
            )

        return (
            Path(__file__).resolve().parents[2]
            / 'data'
            / 'tanzania_locations.json'
        )

    def _required_text(self, data, key, label):

        value = self._text(
            data.get(
                key,
                ''
            )
        )

        if not value:

            raise CommandError(
                f'{label} is missing required key "{key}".'
            )

        return value

    def _text(self, value):

        if value is None:

            return ''

        return str(
            value
        ).strip()
