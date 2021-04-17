class Mediator:
    def __init__(self):
        pass

    def register_drawer(self, drawer):
        self._drawer = drawer

    def register_drawarea(self, drawarea):
        self._drawarea = drawarea

    def update(self):
        self._drawarea.update()
