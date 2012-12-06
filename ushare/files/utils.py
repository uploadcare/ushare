def get_extension(filename):
    try:
        ext = filename.rsplit('.', 1)[1]
    except IndexError:
        ext = u''
    return ext
