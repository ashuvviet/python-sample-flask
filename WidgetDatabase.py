from tinydb import TinyDB, Query


class Widget:
    src:str
    styles:str
    name:str
    tags: [str]
    types: [str]
    

class WidgetDatabase:

    db = TinyDB('static/database.json')
    widgets = []


    def addWidget(self,widget:Widget):
        self.db.table('widgets').insert({'src': widget.src, 'style': widget.styles, 'name' : widget.name, 'tags': widget.tags, 'type': widget.types})

    def getWidget(self, widgetID):
        widget = Query()
        return self.db.table('widgets').search(widget.name == widgetID)

    def getAllWidgets(self):
        return self.db.table('widgets').all()    

    def deleteWidget(self, name):
        self.db.table('widgets').remove({'name': name})

