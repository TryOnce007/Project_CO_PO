def register_filters(app):

    @app.template_filter('getattr')
    def getattr_filter(obj, attr):
        return getattr(obj, attr)
    


def row_to_dict(row, columns):
    return {col: getattr(row, col) for col in columns}