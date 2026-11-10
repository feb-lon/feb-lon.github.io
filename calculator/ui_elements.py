from shiny import ui

from shared import question_circle_fill, type_image_size


def empty_text():
    return ui.tags.div({"style": "height:1.5rem;"})


def spacer(width: float, height: float):
    return ui.tags.div({"style": f"width:{width}rem;height:{height}rem;"})


def element_and_tooltip(tag, space=0, *args):
    return ui.div(
        tag,
        spacer(space, 0),
        ui.tooltip(
            question_circle_fill,
            ui.card(
                args,
                class_="tooltip_card",
            ),
        ),
        class_="tag_and_tooltip",
    )

def dark_type():
    return ui.tags.img(src="dark_type.png", width=type_image_size, class_="tooltip_img")


def bug_type():
    return ui.tags.img(src="bug_type.png", width=type_image_size, class_="tooltip_img")


def fire_type():
    return ui.tags.img(src="fire_type.png", width=type_image_size, class_="tooltip_img")


def normal_type():
    return ui.tags.img(src="normal_type.png", width=type_image_size, class_="tooltip_img")


def water_type():
    return ui.tags.img(src="water_type.png", width=type_image_size, class_="tooltip_img")


def electric_type():
    return ui.tags.img(src="electric_type.png", width=type_image_size, class_="tooltip_img")


def grass_type():
    return ui.tags.img(src="grass_type.png", width=type_image_size, class_="tooltip_img")


def ice_type():
    return ui.tags.img(src="ice_type.png", width=type_image_size, class_="tooltip_img")


def fighting_type():
    return ui.tags.img(src="fighting_type.png", width=type_image_size, class_="tooltip_img")


def poison_type():
    return ui.tags.img(src="poison_type.png", width=type_image_size, class_="tooltip_img")


def ground_type():
    return ui.tags.img(src="ground_type.png", width=type_image_size, class_="tooltip_img")


def flying_type():
    return ui.tags.img(src="flying_type.png", width=type_image_size, class_="tooltip_img")


def psychic_type():
    return ui.tags.img(src="psychic_type.png", width=type_image_size, class_="tooltip_img")


def rock_type():
    return ui.tags.img(src="rock_type.png", width=type_image_size, class_="tooltip_img")


def ghost_type():
    return ui.tags.img(src="ghost_type.png", width=type_image_size, class_="tooltip_img")


def dragon_type():
    return ui.tags.img(src="dragon_type.png", width=type_image_size, class_="tooltip_img")


def steel_type():
    return ui.tags.img(src="steel_type.png", width=type_image_size, class_="tooltip_img")


def other_factors():
    return ui.tags.img(src="gen_5_onward_other_factors.png", width="1000px")
