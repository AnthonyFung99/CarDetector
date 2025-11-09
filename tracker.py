class Tracker:

    def __init__(self):

        self.object_centers = []

    def update(self, object_boxes):

        object_boxes_with_ids = []

        for coordinate_x, coordinate_y, width, height in object_boxes:
            center_x, center_y = (
                coordinate_x + width) // 2, (coordinate_y + height) // 2

            object_id = self._find_object(center_x, center_y)

            if object_id != -1:
                self.object_centers[object_id] = (center_x, center_y)
            else:
                object_id = len(self.object_centers) - 1
                self.object_centers.append((center_x, center_y))
                
            object_boxes_with_ids.append(
                [coordinate_x, coordinate_y, width, height, object_id])

        return object_boxes_with_ids

    def _find_object(self, center_x, center_y):

        for object_id, center in enumerate(self.object_centers):
            distance = ((center_x - center[0])**2 + (center_y - center[1])**2)**0.5

            if distance < 40:
                return object_id
            
        return -1