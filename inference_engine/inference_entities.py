from typing import List


class Serializable:

    def to_json(self):
        pass


class AprilTag(Serializable):

    def __init__(self, _id: int, bbox: tuple = (0, 0, 0, 0)):
        self.id = _id
        self.bbox = BoundingBox(x=bbox[0], y=bbox[1], w=bbox[2], h=bbox[3])

    def to_json(self):
        return {'id': self.id, 'bbox': self.bbox.to_json()}


class Vehicle(Serializable):

    def __init__(self, conf: float, bbox: tuple = (0, 0, 0, 0)):
        self.confidence = conf
        self.bbox = BoundingBox(x=bbox[0], y=bbox[1], w=bbox[2], h=bbox[3])

    def to_json(self):
        return {'confidence': self.confidence, 'bbox': self.bbox.to_json()}


class BoundingBox(Serializable):

    def __init__(self, x: float, y: float, w: float, h: float):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def to_json(self):
        return {'x': self.x, 'y': self.y, 'w': self.w, 'h': self.h}


class InferenceResult(Serializable):

    def __init__(self, april_tags, vehicles):
        self.april_tags: List[AprilTag] = april_tags
        self.vehicles: List[Vehicle] = vehicles

    def to_json(self):
        serialized_april_tags = []
        serialized_vehicles = []
        for april_tag in self.april_tags:
            serialized_april_tags.append(april_tag.to_json())
        for vehicle in self.vehicles:
            serialized_vehicles.append(vehicle.to_json())
        return {'april_tags': serialized_april_tags, 'vehicles': serialized_vehicles}
