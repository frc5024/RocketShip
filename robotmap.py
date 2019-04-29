config = {
    "drivetrain": {
        "rotation_pid": {
            "p": 0.01,
            "i": 0,
            "d": 0
        },
        "forward_rotation_pid": {
            "p": 0.01,
            "i": 0,
            "d": 0
        },
        "motors":{
            "lf":1,
            "lr":2,
            "rf":3,
            "rr":4
        },
        "encoders": {
            "tpr": 360,
            "wheel_circ_ft": 2.094395
        }
    },
    "pcm": {
        "can_id": 11,
        "light_ring": 0,
        "finger":1
    },
    "xbox_controllers": {
        "driver": 0
    },
    "loading_limits": {
        "min_angle": 2,
        "tracking_speed": 0.5,
        "ontrack_speed": 0.9,
        "min_distance": 4.5
    }
}