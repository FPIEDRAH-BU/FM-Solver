from fm_solver.feature_model import feature, restriction, feature_model


def test_feature_model():
    mobile_phone = feature.Feature(identifier=1, name="Mobile Phone")
    calls = feature.Feature(identifier=2, name="Calls")
    gps = feature.Feature(identifier=3, name="GPS")
    screen = feature.Feature(identifier=4, name="Screen")
    media = feature.Feature(identifier=5, name="Media")
    basic = feature.Feature(identifier=6, name="Basic")
    colour = feature.Feature(identifier=7, name="Colour")
    high_resolution = feature.Feature(identifier=8, name="High Resolution")
    camera = feature.Feature(identifier=9, name="Camera")
    mp3 = feature.Feature(identifier=10, name="MP3")

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
            restriction.Root(source=mobile_phone),
            restriction.Mandatory(source=mobile_phone, destination=calls),
            restriction.Optional(source=mobile_phone, destination=gps),
            restriction.Mandatory(source=mobile_phone, destination=screen),
            restriction.Optional(source=mobile_phone, destination=media),
            restriction.Xor(
                source=screen, destination=[basic, colour, high_resolution]
            ),
            restriction.Or(source=media, destination=[camera, mp3]),
            restriction.Excludes(source=basic, destination=gps),
            restriction.Requires(source=camera, destination=high_resolution),
        ],
    )

    assert model.get_feature(5) == media
    assert len(model.get_restrictions_with_source(feature=camera)) == 1
    assert len(model.get_restrictions_with_destination(feature=high_resolution)) == 2
