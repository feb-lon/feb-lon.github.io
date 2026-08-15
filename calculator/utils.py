from math import ceil, floor
from typing import Tuple

from shared import pokemons


# gives upper and lower bounds for the ATK / SPA values we are looking for
# see https://bulbapedia.bulbagarden.net/wiki/Damage#Generation_III for a good overview
def calc_offense_backwards_gen_3(dmg_dealt: int, is_physical: bool, obm: list, ibm: list, defense: int,
                                 base_power: int, offense_stage: int, thick_fat_modifier: float,
                                 enemy_ability_modifier: float) -> Tuple[int, int]:
    # ibm = "inside bracket modifier", the modifiers before the +2 in the formula
    # obm = "outside bracket modifier", the modifiers after the +2 in the formula
    offense_guess_min = dmg_dealt
    offense_guess_max = ceil(dmg_dealt / 0.85) + 1
    for factor in obm:
        offense_guess_min = floor(offense_guess_min / factor)
        offense_guess_max = floor(offense_guess_max / factor) + (0 if factor == 1 else 1)

    offense_guess_min = offense_guess_min - 2
    offense_guess_max = offense_guess_max - 2

    # physical moves always deal at least 1 dmg at this point in the calculation
    if offense_guess_min < 2 and is_physical:
        offense_guess_min = 0

    for factor in ibm:
        offense_guess_min = floor(offense_guess_min / factor)
        offense_guess_max = floor(offense_guess_max / factor) + (0 if factor == 1 else 1)

    offense_guess_min = floor(floor(calc_stat_stages_backwards(floor(int(offense_guess_min * 50 * defense)
                                                                     / int(base_power)), offense_stage)[0]
                                    / thick_fat_modifier) / enemy_ability_modifier)
    offense_guess_max = floor(floor(
        calc_stat_stages_backwards(floor(int((offense_guess_max * 50 + 49) * defense + defense - 1)
                                         / int(base_power)), offense_stage)[1] / thick_fat_modifier + 1)
                              / enemy_ability_modifier + 1)
    return offense_guess_min, offense_guess_max


# gives upper and lower bounds for the ATK / SPA values we are looking for
# see https://bulbapedia.bulbagarden.net/wiki/Damage#Generation_IV for a good overview
def calc_offense_backwards_gen_4(damage_received: int, eff1: float, eff2: float, stab_modifier: float,
                                 crit_modifier: float, effective_def_spd: int, base_power: int,
                                 atk_spa_stage: int, early_mod: float, mid_mod: float, late_mod: float) \
        -> Tuple[int, int]:
    offense_guess_min = damage_received
    offense_guess_max = damage_received

    offense_guess_min = floor(floor(floor(floor(offense_guess_min / late_mod) / eff2) / eff1) / stab_modifier)
    offense_guess_max = ceil(ceil(ceil(ceil(offense_guess_max / late_mod) / eff2) / eff1) / stab_modifier)

    offense_guess_min = ceil(floor(offense_guess_min / mid_mod) / crit_modifier) - 2
    offense_guess_max = ceil(ceil(ceil(offense_guess_max / mid_mod) / 0.85) / crit_modifier) - 2

    offense_guess_min = floor(offense_guess_min / early_mod) * 50 * effective_def_spd
    offense_guess_max = (ceil(offense_guess_max / early_mod) * 50 + 49) * effective_def_spd + effective_def_spd - 1

    offense_guess_min = calc_stat_stages_backwards(floor(offense_guess_min / base_power), atk_spa_stage)[0]
    offense_guess_max = calc_stat_stages_backwards(ceil(offense_guess_max / base_power), atk_spa_stage)[1]

    return offense_guess_min, offense_guess_max


# gives upper and lower bounds for the ATK / SPA values we are looking for
# see https://bulbapedia.bulbagarden.net/wiki/Damage#Generation_V_onward for a good overview
def calc_offense_backwards_gen_5_onward(damage_received: int, effectiveness: float, stab_modifier: float,
                                        crit_modifier: float, effective_def_spd: int, base_power: int,
                                        atk_spa_stage: int, mid_mod: float, late_mod: float) -> Tuple[int, int]:
    offense_guess_min = floor(damage_received / late_mod)
    offense_guess_max = floor(damage_received / late_mod + 1)

    # keep both as in the future they might be different at this point
    offense_guess_min = floor(offense_guess_min / effectiveness - 4)
    offense_guess_max = ceil(offense_guess_max / effectiveness + 4)

    offense_guess_min = floor(offense_guess_min / stab_modifier)
    offense_guess_max = floor(offense_guess_max / stab_modifier)

    # offense guess min gets divided by 1
    offense_guess_max = ceil(offense_guess_max / 0.85)

    offense_guess_min = floor(floor(offense_guess_min / crit_modifier) / mid_mod) - 2
    offense_guess_max = floor(floor(offense_guess_max / crit_modifier + 1) / mid_mod + 1) - 2

    offense_guess_min = offense_guess_min * 50 * effective_def_spd
    offense_guess_max = (offense_guess_max * 50 + 49) * effective_def_spd + effective_def_spd - 1

    offense_guess_min = calc_stat_stages_backwards(floor(offense_guess_min / base_power), atk_spa_stage)[0]
    offense_guess_max = calc_stat_stages_backwards(ceil(offense_guess_max / base_power), atk_spa_stage)[1]

    return offense_guess_min - 1, offense_guess_max + 1


# calculates the part in the damage formula before the +2 and after /50
def calc_ibm_damage(base_damage: int, burned_modifier=1.0, barrier_lightscreen_modifier=1.0,
                    current_weather_modifier=1.0, flash_fire_modifier=1.0, is_physical=False) -> int:
    result = floor(floor(floor(floor(base_damage * flash_fire_modifier)
                               * current_weather_modifier) * barrier_lightscreen_modifier) * burned_modifier)

    result = max(result, 1 if is_physical else 0)  # minimum dmg of 1 only for physical moves at this point
    return result + 2


# calculates the part in the damage formula before the random factor and after +2
def calc_obm_damage_no_randomness(base_damage: int, crit_modifier=1, double_damage_charge_modifier=1,
                                  stab_modifier=1.0, effectiveness_type_1=1.0, effectiveness_type_2=1.0) -> int:
    result = apply(crit_modifier, double_damage_charge_modifier, stab_modifier, effectiveness_type_1,
                   effectiveness_type_2, dmg_val=base_damage)
    return result


# calculates the possible min and max values for the original stat of stat_with_stages
def calc_stat_stages_backwards(stat_with_stages: int, stages: int) -> Tuple[int, int]:
    stat_without_stages = stat_with_stages / (2 + (stages if stages > 0 else 0)) * (
            2 - (stages if stages < 0 else 0))
    if stages < 0:
        original_stat_min = max(ceil(stat_without_stages), 0)
        # -stages increases the result due to stages < 0
        return original_stat_min, original_stat_min - ceil(stages / 2)
    else:
        original_stat_min = max(floor(stat_without_stages), 0)
        return original_stat_min, original_stat_min


# all possible defensive stat modifiers before and including stages aside enigma berry
# https://github.com/pret/pokefirered/blob/338ec9d956fcd39f4bbb361b444ded3eec8e9425/src/pokemon.c#L2437
def calc_defensive_stat_modifiers(stat: int, has_defensive_badge=False,
                                  is_latios_latias_with_soul_dew=False,
                                  is_clamperl_with_dep_sea_scale=False, is_ditto_with_metal_powder=False,
                                  marvel_scale_active=False, move_is_explosion_selfdestruct=False,
                                  defensive_stage=0) -> int:
    result = stat
    if has_defensive_badge: result = floor(1.1 * result)
    if is_latios_latias_with_soul_dew: result = floor(1.5 * result)
    if is_clamperl_with_dep_sea_scale: result = floor(2 * result)
    if is_ditto_with_metal_powder: result = floor(2 * result)
    if marvel_scale_active: result = floor(1.5 * result)
    if move_is_explosion_selfdestruct: result = floor(0.5 * result)

    result = calc_stat_stages(result, defensive_stage)
    return result


# all possible offensive stat modifiers before and including stages aside enigma berry
# https://github.com/pret/pokefirered/blob/338ec9d956fcd39f4bbb361b444ded3eec8e9425/src/pokemon.c#L2437
def calc_offense_stat_modifiers(stat: int, has_type_bonus_item=False,
                                has_offense_badge=False,
                                is_latios_latias_with_soul_dew=False, has_huge_pure_power=False,
                                has_choice_band=False, is_clamperl_with_dep_sea_tooth=False,
                                is_pikachu_with_light_ball=False,
                                is_marowak_cubone_with_thick_club=False,
                                thick_fat_applied=False,
                                has_hustle_plus_minus_guts=False, offense_stage=0) -> int:
    result = stat
    if has_type_bonus_item: result = floor(1.1 * result)
    if has_huge_pure_power: result = floor(2 * result)
    if has_offense_badge: result = floor(1.1 * result)
    if is_latios_latias_with_soul_dew: result = floor(1.5 * result)
    if has_choice_band: result = floor(1.5 * result)
    if is_clamperl_with_dep_sea_tooth: result = floor(2 * result)
    if is_pikachu_with_light_ball: result = floor(2 * result)
    if is_marowak_cubone_with_thick_club: result = floor(2 * result)
    if thick_fat_applied: result = floor(0.5 * result)
    if has_hustle_plus_minus_guts: result = floor(1.5 * result)

    result = calc_stat_stages(result, offense_stage)
    return result


# all possible power modifiers before the general dmg formula
# https://github.com/pret/pokefirered/blob/338ec9d956fcd39f4bbb361b444ded3eec8e9425/src/pokemon.c#L2437
def calc_move_power_modifiers(power: int, has_sport=False,
                              overgrow_blaze_torrent_swarm_active=False) -> int:
    result = power
    if has_sport: result = floor(.5 * result)
    if overgrow_blaze_torrent_swarm_active: result = floor(1.5 * result)

    return result


def apply(*args, dmg_val: int) -> int:
    result = dmg_val
    for arg in args:
        result = floor(result * arg)
    result = max(1, result)
    return result


# biv is my abbreviation for 2 * Base stat + Individual Value (also written: 2 * Base + IVs)
# i use it as it is easier to get both as a package than directly calc the base stat
# (and it does not make a difference for the resulting stat anyway)
def biv_range_hp(level: int, current_stat: int, evs: int) -> Tuple[int, int]:
    return biv_range(level, current_stat - 5 - level, evs, 1)


def biv_range(level: int, current_stat: int, evs: int, nature: float) -> Tuple[int, int]:
    biv_maximum = biv_max(level, current_stat, evs, nature)
    biv_minimum = biv_min(level, current_stat, evs, nature)

    # min > max: should not happen (in that case some of the inputs have to be wrong, user sees result is wrong)
    # min = max: we assume we know the exact biv value
    # min < max: might not be exact boundaries, so we readjust
    if biv_minimum < biv_maximum:
        min_stat = calc_stat(level, 0, biv_minimum, evs, nature)
        max_stat = calc_stat(level, 0, biv_maximum, evs, nature)

        if min_stat < current_stat:
            while calc_stat(level, 0, biv_minimum, evs, nature) < current_stat and biv_minimum <= biv_maximum:
                biv_minimum += 1

        if max_stat > current_stat:
            while calc_stat(level, 0, biv_maximum, evs, nature) > current_stat and biv_minimum <= biv_maximum:
                biv_maximum -= 1

    return biv_minimum, biv_maximum


# the minimum possible 2*Base+IV sum for given level, stat, EVs, nature
def biv_min(level: int, current_stat: int, evs: int, nature: float) -> int:
    biv = min(541, max(22, floor((current_stat +
                                   (0 if nature == 1
                                    else ceil(current_stat / 9) if nature == 0.9
                                    else -floor(current_stat / 11))
                                  - 5)
                                  * 100 / level)
                                 - floor(evs / 4)
                       ))
    return biv


# the maximum possible 2*Base+IV sum for given level, stat, EVs, nature
def biv_max(level: int, current_stat: int, evs: int, nature: float) -> int:
    biv = max(22, min(541, floor(((current_stat
                                  + (0 if not (nature == 0.9 and current_stat % 10 == 0) else 1)
                                  + (0 if nature == 1
                                     else ceil(current_stat / 9) if nature == 0.9
                                     else - floor(current_stat / 11))
                                  - 5)
                                 * 100 + 99) / level)
                                - floor(evs / 4)
                      ))
    return biv


def biv_to_base_min(biv) -> int:
    if type(biv) != int:
        return 0
    else:
        return int(ceil((biv - 31) / 2))


def biv_to_base_max(biv) -> int:
    if type(biv) != int:
        return 0
    else:
        return int(floor(biv / 2))


def calc_dmg_base(level: int, move_power: int, offense: int, defense: int) -> int:
    return floor(floor(floor(2 * level / 5 + 2) * move_power * offense / defense) / 50)


# in case you don't want offense / defense included in the calculation
def calc_base_power(level: int, move_power: int) -> int:
    return floor(2 * level / 5 + 2) * move_power


def calc_stat_stages(stat: int, stages: int) -> int:
    return floor(stat * (2 + (stages if stages > 0 else 0)) / (2 - (stages if stages < 0 else 0)))


# calculate the given pokemon yields, valid formula for generations 2-4
# https://bulbapedia.bulbagarden.net/wiki/Experience#Gain_formula
def calc_xp_yield(pokemon, level: int, opponent_is_trainer: bool, lucky_egg_held=False,
                  is_original_trainer=True) -> int:
    xp_pokemon = floor(pokemons["XP"][pokemon] * level / 7)
    xp = floor(floor(floor(xp_pokemon * (1.5 if lucky_egg_held else 1)) * (1.5 if opponent_is_trainer else 1))
               * (1.5 if not is_original_trainer else 1))
    return xp


# calculation of stats beside HP
# Formula: https://bulbapedia.bulbagarden.net/wiki/Stat#Generation_III_onward
def calc_stat(level: int, base: int, iv: int, ev: int, nature: float) -> int:
    return floor((floor(floor(2 * base + iv + floor(ev / 4)) * level / 100) + 5) * nature)


# hp has a slightly different calculation compared to other stats
def calc_hp(level: int, base: int, iv: int, ev: int) -> int:
    return floor(floor(2 * base + iv + floor(ev / 4)) * level / 100) + 10 + level


def possible_base(base: int):
    return min(max(base, 11), 255)

def possible_base_hp(base: int):
    return min(max(base, 21), 255)


# starting in generation 5, this rounding formula is used for some calculations
def gen_5_round(number_to_round: float) -> int:
    result = int(floor(number_to_round))
    if number_to_round % 1 > .5: result = result + 1
    return result
