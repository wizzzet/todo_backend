def get_siblings(qs, obj_id, infinite=False):
    """Извлекает предыдущий и следующий объект"""
    prev_obj, prev_obj_candidate, next_obj, next_is_next = None, None, None, False

    for obj in qs.iterator():
        if next_is_next:
            next_obj = obj
            break

        if obj.pk == obj_id:
            next_is_next = True
            prev_obj = prev_obj_candidate

        prev_obj_candidate = obj

    if infinite:
        qs = tuple(qs)
        if qs:
            if not next_obj:
                next_obj = qs[0]
            if not prev_obj:
                prev_obj = qs[-1]

    return prev_obj, next_obj
