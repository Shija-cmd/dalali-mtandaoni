DEFAULT_CATEGORIES = (
    'House for Rent',
    'Room for Rent',
    'Plot for Sale',
    'Car for Hire',
)


def seed_default_categories(category_model, stdout=None):

    created_count = 0

    for category_name in DEFAULT_CATEGORIES:

        category, created = category_model.objects.get_or_create(
            name=category_name
        )

        if created:

            created_count += 1

            if stdout:

                stdout.write(
                    f'Creating Category: {category.name}'
                )

    return created_count
