import logging

from Substrate import SubstrateParameters
import pygameSubstrate


def main():
    logging.basicConfig(level=logging.DEBUG)

    colormap = (
        "#201F21", "#262C2E", "#352626", "#372B27",
        "#302C2E", "#392B2D", "#323229", "#3F3229",
        "#38322E", "#2E333D", "#333A3D", "#473329",
        "#40392C", "#40392E", "#47402C", "#47402E",
        "#4E402C", "#4F402E", "#4E4738", "#584037",
        "#65472D", "#6D5D3D", "#745530", "#755532",
        "#745D32", "#746433", "#7C6C36", "#523152",
        "#444842", "#4C5647", "#655D45", "#6D5D44",
        "#6C5D4E", "#746C43", "#7C6C42", "#7C6C4B",
        "#6B734B", "#73734B", "#7B7B4A", "#6B6C55",
        "#696D5E", "#7B6C5D", "#6B7353", "#6A745D",
        "#727B52", "#7B7B52", "#57746E", "#687466",
        "#9C542B", "#9D5432", "#9D5B35", "#936B36",
        "#AA7330", "#C45A27", "#D95223", "#D85A20",
        "#DB5A23", "#E57037", "#836C4B", "#8C6B4B",
        "#82735C", "#937352", "#817B63", "#817B6D",
        "#927B63", "#D9893B", "#E49832", "#DFA133",
        "#E5A037", "#F0AB3B", "#8A8A59", "#B29A58",
        "#89826B", "#9A8262", "#888B7C", "#909A7A",
        "#A28262", "#A18A69", "#A99968", "#99A160",
        "#99A168", "#CA8148", "#EB8D43", "#C29160",
        "#C29168", "#D1A977", "#C9B97F", "#F0E27B",
        "#9F928B", "#C0B999", "#E6B88F", "#C8C187",
        "#E0C886", "#F2CC85", "#F5DA83", "#ECDE9D",
        "#F5D294", "#F5DA94", "#F4E784", "#F4E18A",
        "#F4E193", "#E7D8A7", "#F1D4A5", "#F1DCA5",
        "#F4DBAD", "#F1DCAE", "#F4DBB5", "#F5DBBD",
        "#F4E2AD", "#F5E9AD", "#F4E3BE", "#F5EABE",
        "#F7F0B6", "#D9D1C1", "#E0D0C0", "#E7D8C0",
        "#F1DDC6", "#E8E1C0", "#F3EDC7", "#F6ECCE",
        "#F8F2C7", "#EFEFD0"
    )

    substrate_parameters = SubstrateParameters(height=1080, width=1920, bg_color=(255, 255, 255), max_num=100)
    substrate_parameters.set_color_list(colormap)
    substrate_parameters.wireframe = False
    substrate_parameters.circle_percent = 10

    pygameSubstrate.run(substrate_parameters)


if __name__ == '__main__':
    main()
