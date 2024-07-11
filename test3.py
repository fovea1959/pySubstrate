import logging

from Substrate import SubstrateParameters
import pygameSubstrate


def main():
    logging.basicConfig(level=logging.DEBUG)

    colormap = (
        "#c00000", "#00c000", "#0000c0"
    )

    substrate_parameters = SubstrateParameters(height=1080, width=1920, fg_color=(128, 128, 128), bg_color=(0, 0, 0), max_num=100)
    substrate_parameters.set_color_list(colormap)
    substrate_parameters.wireframe = False
    substrate_parameters.circle_percent = 10

    print(repr(substrate_parameters))

    pygameSubstrate.run(substrate_parameters)


if __name__ == '__main__':
    main()
