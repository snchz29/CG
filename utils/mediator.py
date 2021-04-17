class Mediator:
    def __init__(self):
        self._weight_value_label = None
        self._point_info_widget = None
        self._drawer = None
        self._drawarea = None
        self._weight_slider = None

    def register_info_widget(self, info_widget):
        self._point_info_widget = info_widget

    def register_weight_value_label(self, value_label):
        self._weight_value_label = value_label

    def register_weight_slider(self, weight_slider):
        self._weight_slider = weight_slider

    def register_drawer(self, drawer):
        self._drawer = drawer

    def register_drawarea(self, drawarea):
        self._drawarea = drawarea

    def change_weight_value_label(self, new_value):
        self._weight_value_label.setText(f"Вес точки: {new_value}")

    def change_current_point_weight(self, new_value):
        self._drawer.set_new_current_point_weight(new_value)

    def update(self):
        self._drawarea.update()

    def set_point_info_widget_current_point(self, current_point, idx):
        self._point_info_widget.setVisible(True)
        self._point_info_widget.set_point(idx)
        self._weight_value_label.setText(f"Вес точки: {current_point.get_weight()}")
        self._weight_slider.setValue(current_point.get_weight())