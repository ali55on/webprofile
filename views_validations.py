def separate_posts_into_quantity_groups(
        posts_list: list, items_quantity: int) -> list:
    """Separate on groups

    if quantity groups is 3...
    move this:
    [obj, obj, obj, obj, obj, obj]

    for this:
    [[obj, obj, obj], [obj, obj, obj]]

    :param posts_list:
    :param items_quantity:
    :return:
    """

    all_post_groups_list = []
    one_post_group_list = []
    for item in enumerate(posts_list):
        index_post, object_post = (item[0], item[1])

        if index_post != 0 and index_post % items_quantity == 0:
            all_post_groups_list.append(one_post_group_list)
            one_post_group_list = []

        one_post_group_list.append(object_post)
    all_post_groups_list.append(one_post_group_list)

    return all_post_groups_list


def content_as_p(text: str):
    return '<p>' + text.replace('\n', '</p><p>') + '</p>'


def content_rm_p(text: str):
    return text.replace('<p>', '').replace('</p>', '')
