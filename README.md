# FM-Solver

```Python
from fm_solver import feature_model, translator


mobile_phone = feature_model.Feature(identifier=1, name="Mobile Phone")
calls = feature_model.Feature(identifier=2, name="Calls")
gps = feature_model.Feature(identifier=3, name="GPS")
screen = feature_model.Feature(identifier=4, name="Screen")
media = feature_model.Feature(identifier=5, name="Media")
basic = feature_model.Feature(identifier=6, name="Basic")
colour = feature_model.Feature(identifier=7, name="Colour")
high_resolution_model = feature.Feature(identifier=8, name="High Resolution")
camera = feature_model.Feature(identifier=9, name="Camera")
mp3 = feature_model.Feature(identifier=10, name="MP3")

model = feature_model.FeatureModel(
    features=[
        mobile_phone,
        calls,
        gps,
        screen,
        media,
        basic,
        colour,
        high_resolution,
        camera,
        mp3,
    ],
    restrictions=[
        feature_model.Root(source=mobile_phone),
        feature_model.Mandatory(source=mobile_phone, destination=calls),
        feature_model.Optional(source=mobile_phone, destination=gps),
        feature_model.Mandatory(source=mobile_phone, destination=screen),
        feature_model.Optional(source=mobile_phone, destination=media),
        feature_model.Xor(
            source=screen, destination=[basic, colour, high_resolution]
        ),
        feature_model.Or(source=media, destination=[camera, mp3]),
        feature_model.Excludes(source=basic, destination=gps),
        feature_model.Requires(source=camera, destination=high_resolution),
    ],
)

minizinc_problem = translator.MiniZincArithmeticTranslator(model).translate()

print(minizinc_problem)
```
