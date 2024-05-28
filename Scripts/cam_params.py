#Camera parameters for the Baumer camera used in the implementation to record the feed image
import neoapi
import sys

def get_camera():
    camera = neoapi.Cam()
    camera.Connect()
    camera.f.Width.Set(640)
    camera.f.Height.Set(337)
    camera.f.OffsetX.Set(1056)
    camera.f.OffsetY.Set(1481)

    if camera.f.PixelFormat.GetEnumValueList().IsReadable('Mono8'):
        camera.f.PixelFormat.SetString('Mono8')
    else:
        print('no supported pixelformat')
        sys.exit(0)

    # Ensure SequencerMode is Off
    sequencer_mode = camera.f.SequencerMode.Get()
    if sequencer_mode == 'On':
        camera.f.SequencerMode.Set('Off')

    # Ensure ExposureMode is not TriggerWidth
    exposure_mode = camera.f.ExposureMode.Get()
    if exposure_mode == 'TriggerWidth':
        camera.f.ExposureMode.Set('Timed')

    exposure_auto = camera.f.ExposureAuto.Get()
    if exposure_auto != 1:
        camera.f.ExposureAuto.Set(1)

    # Ensure SequencerConfigurationMode is Off if ExposureAuto is not Off
    sequencer_configuration_mode = camera.f.SequencerConfigurationMode.Get()
    if sequencer_configuration_mode == 'On':
        camera.f.SequencerConfigurationMode.Set('Off')

    # Now try setting the ExposureTime
    try:
        camera.f.ExposureTime.Set(1086)
        camera.SetFeature("Gain", 1)
        print(f"Setting exposure as new")
    except neoapi.neoapi.FeatureAccessException as e:
        print(f"Setting exposure as default")
    return camera
