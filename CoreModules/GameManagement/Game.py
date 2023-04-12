import copy

from CoreModules.NetworkManagement.Echange import echanger, dict_demon, encode_update_packets, \
decode_update_packets, decode_ponctual_packets, encode_walkers_movments_packets, decode_walkers_movments_packets, \
find_key,decode_login_packets, Packet, PacketTypes

from CoreModules.WalkersManagement import walkersManagementWalker as walkers
from CoreModules.BuildingsManagement import buildingsManagementBuilding as buildings
from CoreModules.GameManagement import Update as updates
from Services.servicesmMapSpriteToFile import water_structures_types, farm_types, temple_types, sanitation_types
from Services.Service_Game_Data import building_dico, road_dico, removing_cost
from Services import Service_Save_and_Load as save_and_load
from Services import Service_Save_and_Load as saveLoad
import time
import random
from Services.Service_Static_functions import position_is_valid
from Services import servicesGlobalVariables as globalVar
import struct


INIT_MONEY = 100000000
TIME_BEFORE_REMOVING_DWELL = 1.5  # seconds



class Game:
    def __init__(self, _map, name="save", owner_id=None, is_online=False):
        self.name = name
        self.map = _map
        self.startGame()
        self.scaling = 0
        self.owner = owner_id
        print(self.owner)
        self.is_online = is_online
        self.money = INIT_MONEY
        self.food = 0
        self.potery = 0
        self.likeability = 0
        self.gods_favors = [0, 0, 0, 0, 0]
        self.caesar_score = 0
        self.unemployement = 0
        self.isPaused = False
        self.buildinglist = []
        self.walkersAll = []
        self.walkersOut = []
        self.unemployedCitizens = []

        self.framerate = globalVar.DEFAULT_FPS
        self.updated = []
        self.players = [(self.owner, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                        (('127.0.0.1', 1000), (255, 0, 0))]
        # some lists of specific buildings
        self.dwelling_list = []

        self.water_structures_list = []
        self.food_structures_list = []
        self.temple_structures_list = []
        self.education_structures_list = []
        self.fountain_structures_list = []
        self.basic_entertainment_structures_list = []
        self.pottery_structures_list = []
        self.bathhouse_structures_list = []

        self.granary_list = []
        self.prefecture_list = []
        self.farm_list = []
        self.reservoir_list = []
        self.military_list = []

        #
        self.last_water_structure_removed = None
        self.last_food_structure_removed = None
        self.last_temple_structure_removed = None
        self.last_education_structure_removed = None
        self.last_fountain_structure_removed = None
        self.last_basic_entertainment_structure_removed = None
        self.last_pottery_structure_removed = None
        self.last_bathhouse_structure_removed = None
        self.last_reservoir_removed = None

        # Timer
        self.init_time = time.time()
        self.timer_for_immigrant_arrival = {}
        self.tmp_ref_time = time.time()
        # a dic of timers to track dwells with no roads
        # it associates each position of dwell with a timer
        self.timer_track_dwells = {}

        self.paths_for_buildings = {}

        self.total_food = 0

        self.queue_exit = []

    def add_player(self, id_player, color):
        if (id_player, color) not in self.players:
            self.players.append((id_player, color))

    def update_food_qty(self):
        self.total_food = sum(gran.storage for gran in self.granary_list)
        return self.total_food

    def get_dwell_count(self):
        return len(self.dwelling_list)

    def startGame(self):
        # ---------------------------------#
        _path = self.map.path_entry_to_exit(self.map.roads_layer.get_entry_position(),
                                            self.map.roads_layer.get_exit_position())
        self.map.roads_layer.build_path_entry_to_exit(
            _path, [self.map.hills_layer, self.map.trees_layer])

    def change_game_speed(self, step):
        """
        A step of 1 indicates incremental speed
        And -1 indicates decremental speed
        """
        if self.framerate > globalVar.DEFAULT_FPS:
            if step == 1 and self.framerate < 10 * globalVar.DEFAULT_FPS:
                self.framerate += globalVar.DEFAULT_FPS
            elif step == -1:
                self.framerate -= globalVar.DEFAULT_FPS
        elif self.framerate < globalVar.DEFAULT_FPS:
            if step == 1:
                self.framerate += 0.1 * globalVar.DEFAULT_FPS
            elif step == -1 and self.framerate > 0.1 * globalVar.DEFAULT_FPS:
                self.framerate -= 0.1 * globalVar.DEFAULT_FPS
        else:
            if step == 1:
                self.framerate += globalVar.DEFAULT_FPS
            elif step == -1:
                self.framerate -= 0.1 * globalVar.DEFAULT_FPS

    def foodproduction(self):
        # ---------------------------------#
        pass

    def updatebuilding(self, building: buildings.Building):
        current_state = (building.isBurning, building.isDestroyed, building.risk_level_dico["fire"],
                         building.risk_level_dico["collapse"])
        if not building.isDestroyed:
            building.update_risk("fire")
            building.update_risk("collapse")
        updated_state = (building.isBurning, building.isDestroyed, building.risk_level_dico["fire"],
                         building.risk_level_dico["collapse"])
        dico_change = {"fire": current_state[0] != updated_state[0],
                       "collapse": current_state[1] != updated_state[1],
                       "fire_level": (current_state[2] != updated_state[2], building.risk_level_dico["fire"]),
                       "collapse_level": (current_state[3] != updated_state[3], building.risk_level_dico["collapse"])
                       }
        return dico_change

    def updateReligion(self):
        pass

    def print_building_list(self):
        for b in self.buildinglist:
            print(b.dic['version'])

    def update_supply_requirements_with_structure_range(self, of_what: 'water' or 'food' or 'temple' or 'education'
                                                                       or 'fountain' or 'basic_entertainment' or 'pottery' or 'bathhouse',
                                                        spec_building):
        """
        This functions searches for supply structures on the map and for each one look for dwell within the range of
        the structure. If the dwell required a structure of this type, then its position will be added to the list of
        buildings to update.
        return: a set of positions of housings that will be updated, to avoid duplicate values
        """
        tmp = of_what + '_structures_list'
        structures_list = getattr(self, tmp)
        if spec_building in structures_list:
            self.intermediate_update_supply_function(
                of_what, spec_building, evolvable=True)
        """
        for structure in structures_list:
            if not structure.is_functional():
                continue
            self.intermediate_update_supply_function(of_what, structure, evolvable=True)
        """

    def intermediate_update_supply_function(self, of_what: 'water' or 'food' or 'temple' or 'education' or 'fountain' or
                                                           'basic_entertainment' or 'pottery' or 'bathhouse', structure,
                                            evolvable=True):
        if structure:  # None
            if structure.is_functional():
                _range = structure.range
                _position = structure.position

                for dwelling in self.dwelling_list:
                    line, column = dwelling.position
                    if -_range + _position[0] <= line < _range + 1 + _position[0] and -_range + _position[1] <= column \
                            < _range + 1 + _position[1]:
                        dwelling.update_requirements()
                        status = dwelling.update_with_supply(
                            of_what, evolvable=evolvable)

    def update_water_for_fountain_or_bath(self, reservoir, update, evolvable=True):
        if reservoir and reservoir.is_functional():  # None
            _range = reservoir.range
            _position = reservoir.position
            for fountain_bath in self.water_structures_list:
                if fountain_bath.dic['version'] in sanitation_types:
                    line, column = fountain_bath.position
                    if -_range + _position[0] <= line < _range + 1 + _position[0] and \
                            -_range + _position[1] <= column < _range + 1 + _position[1]:
                        if fountain_bath.set_functional(evolvable):
                            
                            update.has_evolved.append((fountain_bath.position, fountain_bath.structure_level))

    def downgrade_supply_requirement_with_structure_range(self, of_what: 'water' or 'food' or 'temple' or
                                                                         'education' or 'fountain' or 'basic_entertainment' or 'pottery' or 'bathhouse'):
        tmp = 'last_' + of_what + '_structure_removed'
        structure = getattr(self, tmp)
        if structure:
            self.intermediate_update_supply_function(
                of_what, structure, evolvable=False)
            setattr(self, tmp, None)

    def downgrade_supply_requirement_with_walker(self, supply):
        for dwelling in self.dwelling_list:
            dwelling.update_requirements()
            status = dwelling.update_with_supply(supply, evolvable=False)

    def workers_create(self, k, possible_road, has_road, should_wait=False):
        worker_job = None
        match k.dic['version']:
            case "engineer's_post":
                worker_job = "engineer"
            case "prefecture":
                worker_job = "prefect"
            case _ if k.dic['version'] in temple_types:
                worker_job = "priest"
            case "granary":
                worker_job = "market_trader"
            case "military_academy":
                worker_job = "soldier"
            case _ if k.dic['version'] in farm_types:
                worker_job = "pusher_wheat"

        # if k.dic['version']=="granary": print(f"Has road={has_road} -- Number of employees={k.current_number_of_employees} ")
        if worker_job and has_road and k.current_number_of_employees < k.max_number_of_employees \
                and not k.isDestroyed and not k.isBurning:
            # if k.dic['version']=="military_academy":print(f"{k.current_number_of_employees} vs {k.max_number_of_employees}")

            if self.unemployedCitizens:
                citizen = random.choice(self.unemployedCitizens)
                worker = citizen.change_profession(worker_job)
                self.walkersAll.remove(citizen)
                self.unemployedCitizens.remove(citizen)

                self.walkersAll.append(worker)
                self.walkersAll = list(set(self.walkersAll))

                worker.set_working_building(k)
                k.add_employee(worker.id, update_number=True, e_object=worker)
                if not k.is_functional():
                    k.set_functional(True)

                a = random.randint(0, len(possible_road) - 1)
                worker.init_pos = possible_road[a]
                self.walkersGetOut(worker)
                if should_wait:
                    worker.wait = True
                return True
            return False

    def actions_on_buildings(self, buildinglist, update, update_to_send):
        for k in buildinglist:
            if True:
                # Some variables that will be used
                if isinstance(k, buildings.Farm | buildings.Granary):
                    voisins = self.get_voisins_tuples(k, offset=1)
                else:
                    voisins = self.get_voisins_tuples(k)
                possible_roads = [
                    v for v in voisins if self.map.roads_layer.is_real_road(v[0], v[1])]
                has_road = len(possible_roads) != 0
                pos = k.position

                # =======================================
                #  Updates of the requirements
                # =======================================
                if k in self.water_structures_list:
                    self.update_supply_requirements_with_structure_range(
                        'water', k)
                if k in self.bathhouse_structures_list:
                    self.update_supply_requirements_with_structure_range(
                        'education', k)
                if k in self.fountain_structures_list:
                    self.update_supply_requirements_with_structure_range(
                        'fountain', k)
                if k in self.basic_entertainment_structures_list:
                    self.update_supply_requirements_with_structure_range(
                        'basic_entertainment', k)
                if k in self.bathhouse_structures_list:
                    self.update_supply_requirements_with_structure_range(
                        'bathhouse', k)
                if k in self.reservoir_list:
                    self.update_water_for_fountain_or_bath(k, update=update)

                # Update of the risk speed level
                k.update_risk_speed_with_level()

                # Update of animation
                k.update_functional_building_animation()

                # Reset working building with no employee
                if k.need_employee and k.current_number_of_employees == 0 and k.is_functional():
                    k.set_functional(False)

                # =======================================
                #  Creation of immigrants
                # =======================================
                if type(k) == buildings.Dwelling and not k.isDestroyed and not k.isBurning and \
                        k.current_number_of_employees < k.max_number_of_employees and has_road:
                    if k not in self.paths_for_buildings.keys():
                        self.paths_for_buildings[k] = \
                            self.map.walk_to_a_building(self.map.roads_layer.get_entry_position(),
                                                        None, k.position, [], walk_through=True)[1]

                    else:
                        path = self.paths_for_buildings[k]
                        if path and (time.time() - self.tmp_ref_time) > 0.1:
                            self.tmp_ref_time = time.time()
                            # We call the required number of immigrants sequentially but with a delay of 2s to render
                            if k not in self.timer_for_immigrant_arrival.keys():
                                self.timer_for_immigrant_arrival[k] = time.time(
                                )
                            current_time = time.time()
                            if int(current_time - self.timer_for_immigrant_arrival[k]) > 0.3:
                                self.create_immigrant(path.copy(), k)
                                self.timer_for_immigrant_arrival[k] = current_time
                                # We remove the timer associated to this house if the max_population is reached
                                if k.current_number_of_employees == k.max_number_of_employees:
                                    del self.timer_for_immigrant_arrival[k]
                                    del self.paths_for_buildings[k]

                # ======================================================
                #  Creation of prefects, engineers, priests and traders, and soldiers
                # ======================================================
                if k.dic['version'] in ["engineer's_post", "prefecture", "granary", "military_academy"] + temple_types:
                    self.workers_create(k, possible_roads, has_road)

                # =======================================
                #  Creation of cart_pushers
                # =======================================
                elif k.dic['version'] in farm_types:
                    if k.in_state_0():
                        k.stop_production = True
                        if self.workers_create(k, possible_roads, has_road, should_wait=True):
                            k.stop_production = False

                    else:
                        pusher = list(k.get_all_employees(real_object=True))[0]

                        if k.in_state_1():
                            self.workers_create(
                                k, possible_roads, has_road, should_wait=True)

                        elif k.in_state_2(pusher):
                            k.stop_production = False

                        elif k.in_state_3(pusher):
                            # Stop animation and production and the cart pusher working in it look for a granary
                            k.stop_production = True
                            found_granary = False
                            for granary in self.granary_list:
                                # print(f"Hey, Granary functional = {granary.is_functional()} -- storage is = ",
                                # granary.storage, f" and full? = {granary.is_full()}")
                                if granary.is_functional() and not granary.is_full():
                                    STATUS = pusher.move_to_another_dwell(granary.position)
                                    # print(f"Pathfinding:{STATUS}")
                                    if STATUS:
                                        found_granary = True
                                        pusher.transition_building = granary
                                        break
                            if found_granary:
                                pusher.wait = False
                                # print("reset anim etat2"+str(k.reset_animation))
                                k.reset_animation = True
                                k.stop_production = False
                                """
                                print(f"Variables booleenes:\n Number_of_employees={k.current_number_of_employees} \n "
                                f"Haverstable = {k.is_haverstable()} \n Destroyed={k.isDestroyed} \n Burning={k.isBurning}\n"
                                f"Stop production = {k.stop_production} \n Pusher waiting={pusher.wait} \n Reset_animation = {k.reset_animation}")
                                """
                            else:
                                # print("Je ne trouve pas de grenier")
                                k.stop_production = True

                        elif k.in_state_4(pusher):
                            # print("Etat4")
                            # The cart pusher found a granary and is walking toward it
                            # Reset animation
                            k.structure_level = 0
                            k.quantity = 0
                            k.stop_production = False
                            k.reset_animation = False

                        elif k.in_state_5(pusher) and not pusher.transition_building:
                            # pusher returned
                            # print("Etat5")
                            pusher.wait = True

                # =======================================
                #  Control of dwellings with no access to roads
                # =======================================
                if type(k) == buildings.Dwelling and not k.is_occupied():
                    # we check if a road is next to this dwelling, if not we remove it after Xs
                    removable = True
                    for i, j in voisins:
                        if self.map.roads_layer.is_real_road(i, j):
                            removable = False
                            break
                    # update tracktimer of dwells
                    built_since = int(
                        time.time() - self.timer_track_dwells[pos]) if pos in self.timer_track_dwells else 0

                    if removable and built_since > TIME_BEFORE_REMOVING_DWELL:
                        # to avoid decreasing money
                        self.money += removing_cost
                        self.remove_element(pos)
                        update.removed.append(pos)
                        self.timer_track_dwells.pop(pos)

                    elif built_since > TIME_BEFORE_REMOVING_DWELL:
                        self.timer_track_dwells.pop(pos)

                # =======================================
                #  Update of burnt and collapsed buildings
                # =======================================
                building_update = self.updatebuilding(k)
                # The fire and collapse risks are updated but graphically only for the buildings owned by the player
                # Other players should be updated graphically only when they send their updates
                if k.owner == self.owner:
                    cases = self.map.buildings_layer.get_all_positions_of_element(
                        pos[0], pos[1])
                    if building_update["fire"]:                        
                        # the building is no more functional
                        k.functional = False
                        for i in cases:                            
                            self.map.buildings_layer.array[i[0]
                                                        ][i[1]].isBurning = True
                            update.catchedfire.append(i)
                        self.guide_homeless_and_jobless_citizens(k)

                    if building_update["collapse"]:
                        # the building is no more functional
                        k.functional = False
                        for i in cases:
                            self.map.buildings_layer.array[i[0]
                                                        ][i[1]].isDestroyed = True                            
                            update.collapsed.append(i)
                        self.guide_homeless_and_jobless_citizens(k)

                if building_update["fire_level"][0]:
                    update.fire_level_change.append(
                        (k.position, building_update["fire_level"][1]))
                if building_update["collapse_level"][0]:
                    update.collapse_level_change.append(
                        (k.position, building_update["collapse_level"][1]))

                # =======================================
                # Managment of burning houses
                # =======================================
                prefets = self.get_prefets()
                if k.isBurning and not k.fire_fighter_is_coming:
                    for prefet in prefets:
                        if not prefet.work_target:
                            if prefet.move_to_another_dwell(k.position):
                                prefet.work_target = k
                                k.fire_fighter_is_coming = True
                            break

                # And a final update of all buildings
                update.has_evolved.append((k.position, k.structure_level))
                if k.dic['version'] in ['dwell']:
                    update_to_send.has_evolved.append((k.position, k.structure_level))
                

    def updategame(self, scaling):
        """
        This function updates the game
        In fact it updates the buildings of the game but also the walkers
        Differents types of updates can occur: a building evolving, a building burning or a building collapsing
        """
        walkers.clear_shared_object()
        
        self.scaling = scaling
        self.update_food_qty()
        
        # The important object that will contain the updates
        update = updates.LogicUpdate()
        # =======================================
        #  Updates of the walker
        # =======================================

        if self.queue_exit:
            self.queue_exit = [
                non_citizen for non_citizen in self.queue_exit if not non_citizen.exit_way()]

        walker_to_update = set()
        for walker in self.walkersOut:
            if not walker.wait:
                status = walker.walk(self.scaling)
                if status == globalVar.IMMIGRANT_INSTALLED:
                    # An immigrant just set up --
                    new_status = walker.settle_in()
                    if new_status:
                        self.walkersAll.remove(walker)
                        self.walkersAll.append(new_status)
                        # we add a citizen as an unemployed
                        self.unemployedCitizens.append(new_status)

                elif status == globalVar.CITIZEN_IS_OUT:
                    walker_to_update.add(walker)

                elif status == globalVar.CITIZEN_ARRIVED:
                    # When a citizen arrives at a target building position, we make him wait 3s so that to
                    # easily perceive that
                    # If the target building is destroyed or burned or removed when he comes by, we should pay attention
                    # not to make actions on this building
                    walker.wait = True
                    walker.beg_loading_ref = time.time()

                    # Special walkers
                    if isinstance(walker, walkers.Prefect):
                        walker.instinguish_fire()
                        walker.work_target.fire_fighter_is_coming = False
                        update.collapsed.append(walker.work_target.position)
                        walker.work_target = None

                    elif isinstance(walker, walkers.Cart_Pusher_Wheat):
                        granary = walker.transition_building
                        if granary:
                            walker.transition_building = None
                            walker.move_to_another_dwell(
                                walker.work_building.position)
                            if not (granary.isDestroyed or granary.isBurning):
                                granary.inc_storage()

                    elif isinstance(walker, walkers.Market_Trader):
                        # a market trader arrived to his granary building
                        if not (walker.work_building.isDestroyed or walker.work_building.isBurning):
                            a = walker.work_building.dec_storage()
                            walker.products_qty += a

                    elif isinstance(walker, walkers.Soldier):
                        tmp = walker.work_target
                        if tmp and not tmp.isDestroyed:
                            tmp.automatic_destruction()
                            walker.work_target = None
                            walker.move_to_another_dwell(
                                walker.work_building.position)
                        elif not tmp:
                            # in casern
                            walker.going_back_mlt = True

                elif status is None:
                    if type(walker) in [walkers.Prefect, walkers.Engineer]:
                        walker.work(self.get_buildings_for_walker_with_offset(
                            walker.init_pos, type(walker)), update)

                    elif isinstance(walker, walkers.Priest | walkers.Market_Trader):
                        dwells_around = [b for b in
                                         self.get_buildings_for_walker_with_offset(
                                             walker.init_pos, type(walker))
                                         if b.dic['version'] == "dwell"]
                        walker.work(dwells_around, update)
            else:
                # The cart pusher and the market trader should go
                if isinstance(walker, walkers.Soldier) and walker.going_back_mlt:
                    continue
                if walker.beg_loading_ref and time.time() - walker.beg_loading_ref > 3:
                    walker.wait = False
                    walker.beg_loading_ref = None

        for w_to_update in walker_to_update:
            w_to_update.get_out_city()

        # =======================================
        #  Updates of the requirements
        # =======================================
        self.downgrade_supply_requirement_with_structure_range('water')
        if self.granary_list == []:
            self.downgrade_supply_requirement_with_walker('food')
        if self.temple_structures_list == []:
            self.downgrade_supply_requirement_with_walker('temple')

        self.downgrade_supply_requirement_with_structure_range('fountain')
        self.downgrade_supply_requirement_with_structure_range(
            'basic_entertainment')
        self.downgrade_supply_requirement_with_structure_range('bathhouse')

        # -------------------------------------------------------------------------------------------------#
        # Updating of water structures wich functionality depends on a reservoir presence
        # Typically fountains
        # -------------------------------------------------------------------------------------------------#
        if self.last_reservoir_removed:
            self.update_water_for_fountain_or_bath(self.last_reservoir_removed, update=update,evolvable=False)
            self.last_reservoir_removed = None

        # ---------------------------------------------------------
        # Main loop that check each building built
        # ---------------------------------------------------------

        size = len(self.buildinglist)
        building_list1 = self.buildinglist[:size // 2]
        building_list2 = self.buildinglist[size // 2:]

        # Reduced update object to send when online
        # On purpose, it contains has_evolved type updates, only for dwells
        # It does not neither contain risk changes of buildings
        update_to_send = updates.LogicUpdate()
        
        self.actions_on_buildings(building_list1, update, update_to_send=update_to_send)
        self.actions_on_buildings(building_list2, update, update_to_send=update_to_send)
        
        update.has_evolved = list(set(update.has_evolved))
        # ---------------------------------------------------------
        # Sending updates to other players
        # ---------------------------------------------------------

        #update_to_send.fire_level_change = update.fire_level_change
        #update_to_send.collapse_level_change = update.collapse_level_change
        update_to_send.collapsed = update.collapsed
        update_to_send.catchedfire = update.catchedfire
        update_to_send.removed = update.removed

        if self.is_online:
            sending_update_packets = encode_update_packets(update_to_send)
            walkers_packets = encode_walkers_movments_packets(walkers.shared_walker_mvt_updates)
            #self.send_update_packets(sending_update_packets + walkers_packets)
            #self.send_update_packets(sending_update_packets)

            # ---------------------------------------------------------
            # Receiving updates from other players
            # ---------------------------------------------------------
            incoming_packets = [ echanger.receive() for _ in range(echanger.getter_current_messages()[0]) ]
            #print(incoming_packets)
            layers_to_update_from_packets= self.include_incoming_packets(incoming_packets,update)
            return update, layers_to_update_from_packets
        return update


    def attack(self, building_pos):
        if (len(self.military_list) != 0):
            for soldier in self.walkersOut:
                if isinstance(soldier, walkers.Soldier):
                    building = self.map.buildings_layer.get_cell(
                        building_pos[0], building_pos[1])
                    soldier.s_work(building)
                    return

    def get_citizen_by_id(self, id: int):
        for ctz in self.walkersAll:
            if ctz.id == id:
                return ctz

    def guide_homeless_and_jobless_citizens(self, building):
        """
        Note: Retire les citoyens même s'ils ne sont pas effectivement sortis
        """
        if type(building) == buildings.Dwelling:
            for ctz_id in building.get_all_employees(real_object=False):
                ctz = self.get_citizen_by_id(ctz_id)
                #ctz = ctz_id
                if isinstance(ctz, walkers.Soldier):
                    self.going_back_mlt = False
                ctz.wait = False
                if ctz.exit_way() == [] or ctz.exit_way == None:
                    self.queue_exit.append(ctz)
                if ctz in self.unemployedCitizens:
                    self.unemployedCitizens.remove(ctz)
                if ctz.work_building:
                    ctz.work_building.rem_employee(ctz_id, e_object = ctz)
                self.walkersGetOut(ctz)
            building.flush_employee()

        else:
            for ctz_id in building.get_all_employees(real_object=False):
                ctz = self.get_citizen_by_id(ctz_id)
                #ctz = ctz_id
                if isinstance(ctz, walkers.Soldier):
                    self.going_back_mlt = False
                if building.dic['version'] == "military_academy":
                    print("BATARD DEGAGE")
                ctz.wait = False
                # Return in its house
                ctz.move_to_another_dwell(
                    ctz.house.position, walk_through=True)
                self.walkersAll.remove(ctz)
                if ctz in self.walkersOut:
                    self.walkersOut.remove(ctz)
                ctz = ctz.change_profession("citizen")
                self.walkersAll.append(ctz)
                self.walkersAll = list(set(self.walkersAll))
                self.unemployedCitizens.append(ctz)
                ctz.work_building = None
                self.walkersGetOut(ctz)
                break
            building.flush_employee()

    def get_buildings_for_walker_with_offset(self, walker_position, walker_class):
        match walker_class:
            case walkers.Market_Trader, walkers.Cart_Pusher_Wheat:
                right_range = range(-1, 2)

            case _:
                right_range = range(-2, 3)

        tmp = [(walker_position[0] + i, walker_position[1] + j)
               for i in right_range for j in right_range]
        building_where_to_work = []
        for b in self.buildinglist:
            if b.position in tmp:
                building_where_to_work.append(b)
        return building_where_to_work

    def create_immigrant(self, path=[], building=None, display=False):
        walker = walkers.Immigrant(self.map.roads_layer.get_entry_position()[0], self.map.roads_layer.get_entry_position()[1],
                                   None, 0, self, path, building)
        self.walkersAll.append(walker)
        self.walkersAll = list(set(self.walkersAll))
        self.walkersGetOut(walker)

    def walkersGetOut(self, walker):
        self.walkersOut.append(walker)
        self.walkersOut = list(set(self.walkersOut))
        pass

    def walkersOutUpdates(self, exit=False):  # fps = self.framerate
        pass

    def remove_element(self, pos, from_packet = False) -> str | None:
        """
        Cette fonction permet d'enlever un element de la map à une position donnée
        On ne peut pas retirer de l'herbe ou une montagne
        """
        line, column = pos[0], pos[1]
        layer_type, _element = self.map.get_element_in_cell(line, column)
        # Ownership rights
        # Implementation choice:: Everyone can remove a road whoever its owner is
        # Nobody can remove trees
        if layer_type != globalVar.LAYER4 and _element and _element.owner != self.owner and not from_packet:
            print("Not your building")
            return None
        
        if self.money < removing_cost:
            print("Not enough money")
            return None
        
        status, element_type, _element = self.map.remove_element_in_cell(
            line, column)
        if status:
            if not from_packet: self.money -= removing_cost
            if element_type == globalVar.LAYER5:
                if self.buildinglist:
                    """
                    # to remove the time tracker if the building is removed before 3s
                    if pos in self.timer_track_dwells:
                        self.timer_track_dwells.pop(pos)
                    """
                    self.buildinglist.remove(_element)
                    self.guide_homeless_and_jobless_citizens(_element)

                    if type(_element) == buildings.Dwelling:
                        self.dwelling_list.remove(_element)

                    if type(_element) == buildings.WaterStructure:
                        # we must copy the element because if will potentially be  removed or changed in memory
                        self.last_water_structure_removed = copy.copy(_element)
                        self.water_structures_list.remove(_element)
                        if _element.dic['version'] == "reservoir":
                            self.last_reservoir_removed = copy.copy(_element)
                            self.reservoir_list.remove(_element)

                    if type(_element) == buildings.Granary:
                        self.granary_list.remove(_element)
                    if type(_element) == buildings.Temple:
                        self.temple_structures_list.remove(_element)
                    if _element.dic["version"] == "prefecture":
                        self.prefecture_list.remove(_element)
                    if _element.dic['version'] in farm_types:
                        self.farm_list.remove(_element)
                    if type(_element) == buildings.MilitaryAc:
                        self.military_list.remove(_element)
                    del _element
                    if self.is_online:
                        if not from_packet:
                            body = [line ,column]
                            packet =  Packet(bytearray(body),0,self.owner[0],"255.255.255.255",packetType=PacketTypes.Supprimer)
                            echanger.send(packet)

        return element_type

    def remove_elements_serie(self, start_pos, end_pos) -> set:
        """
        Pour clean une surface de la carte
        Elle va renvoyer un ensemble set qui contient les layers qui ont été modifiés
        """
        line1, column1 = start_pos[0], start_pos[1]
        line2, column2 = end_pos[0], end_pos[1]

        # 2 ranges qui vont servir à délimiter la surface de la map à clean
        vrange, hrange = None, None

        # le set
        _set = set()

        if line1 >= line2:
            vrange = range(line1, line2 - 1, -1)
        else:
            vrange = range(line2, line1 - 1, -1)

        if column1 <= column2:
            hrange = range(column2, column1 - 1, -1)
        else:
            hrange = range(column1, column2 - 1, -1)

        for i in vrange:
            for j in hrange:
                result = self.remove_element((i, j))
                if result:
                    _set.add(result)
        return _set

    def add_road(self, line, column,from_packet = False) -> bool:
        # Precondition: we must have enough money for adding a road
        if self.money < road_dico['cost']:
            print("Not enough money")
            return False
        status = self.map.roads_layer.set_cell_constrained_to_bottom_layer(
            self.map.collisions_layers, line, column)
        if status:
            self.money -= road_dico['cost']
            if self.is_online:
                if not from_packet:
                    body = [line ,column]
                    # The packet should be sent to everyone
                    packet = Packet(bytearray(body),0,self.owner[0],"255.255.255.255",packetType=PacketTypes.Ajout_Route)
                    echanger.send(packet)

        return status

    def add_roads_serie(self, start_pos, end_pos, dynamically=False) -> bool:
        # Here we can't precisely calculate the money that will be needed to construct all the roads. we'll estimate
        # that
        estimated_counter_roads = (
            abs(start_pos[0] - end_pos[0])) + (abs(start_pos[1] - end_pos[1])) + 1
        if self.money < estimated_counter_roads * road_dico['cost']:
            print("Not enough money")
            return False

        status, count = self.map.roads_layer.add_roads_serie(start_pos, end_pos,
                                                             self.map.collisions_layers, memorize=dynamically)

        if status and not dynamically:
            self.money -= road_dico['cost'] * count
        return status

    def add_building(self, line, column, version, from_packet = False) -> bool:
        txt= " ".join(version.split("_"))
        if self.money < building_dico[txt].cost:
            print("Not enough money")
            return False
        # we have to determine the exact class of the building bcause they have not the same prototype
        if version == "dwell":
            building = buildings.Dwelling(
                self.map.buildings_layer, globalVar.LAYER5)
        elif version in water_structures_types:
            building = buildings.WaterStructure(
                self.map.buildings_layer, globalVar.LAYER5, version)
        elif version in farm_types:
            building = buildings.Farm(
                self.map.buildings_layer, globalVar.LAYER5, version)
        elif version == "granary":
            building = buildings.Granary(
                self.map.buildings_layer, globalVar.LAYER5)
        elif version in temple_types:
            building = buildings.Temple(
                self.map.buildings_layer, globalVar.LAYER5, version)
        elif version == "military_academy":
            building = buildings.MilitaryAc(
                self.map.buildings_layer, globalVar.LAYER5)
        else:
            building = buildings.Building(
                self.map.buildings_layer, globalVar.LAYER5, version)
        
        if not from_packet:
            building.owner = self.owner
        else:
            # we should receive ip of the player who constructed
            building.owner = self.identify_owner(from_packet)
            
            
        # we should check that there is no water on the future positions
        cells_number = building.dic['cells_number']
        can_build_out_of_water = all([not self.map.grass_layer.cell_is_water(line + i, column + j)
                                      for j in range(0, cells_number) for i in range(0, cells_number)])
        if not can_build_out_of_water:
            return False

        if version in farm_types:
            # we should check if there is yellow grass on the future positions to check
            can_build_on_yellow_grass = all([self.map.grass_layer.cell_is_yellow_grass(line + i, column + j)
                                             for j in range(0, cells_number) for i in range(0, cells_number)])

            if not can_build_on_yellow_grass:
                return False

        status = self.map.buildings_layer.set_cell_constrained_to_bottom_layer(self.map.collisions_layers, line, column,
                                                                               building)
        if status:
            if not from_packet: self.money -= building_dico[txt].cost
            self.buildinglist.append(building)
            if version == "dwell":
                # if user just built a dwell we associate a timer so that the dwell can be removed after x seconds
                self.timer_track_dwells[(line, column)] = time.time()
                self.dwelling_list.append(building)

            if type(building) == buildings.WaterStructure:
                self.water_structures_list.append(building)
                if building.dic['version'] == "reservoir":
                    self.reservoir_list.append(building)
                    # Functionality of a reservoir is calculated directly when it's created
                    # A reservoir is functional when adjacent to a river or a coast (water)
                    ajacent_to_water = any([self.map.grass_layer.cell_is_water(line + i, column + j)
                                            for j in range(-1, cells_number+1) for i in range(-1, cells_number+1) if i in [-1, cells_number]
                                            or j in [-1, cells_number]])
                    if ajacent_to_water:
                        building.set_functional(True)

            if type(building) == buildings.Granary:
                self.granary_list.append(building)
            if type(building) == buildings.Temple:
                self.temple_structures_list.append(building)
            if building.dic["version"] == "prefecture":
                self.prefecture_list.append(building)
            if building.dic['version'] in farm_types:
                self.farm_list.append(building)
            if type(building) == buildings.MilitaryAc:
                self.military_list.append(building)
           
            if self.is_online:
                if not from_packet:
                    body = [building.position[0],building.position[1],find_key(building.dic["version"],dict_demon)]
                    print(body)
                    packet = Packet(bytearray(body),0,self.owner[0],"255.255.255.255",packetType=PacketTypes.Ajouter)
                    echanger.send(packet)
            
        return status

    def get_buildings_in_neighboorhood(self, pos):
        pass

    def get_voisins_tuples(self, building, offset=2):
        voisins_tuples = set()
        pos_x, pos_y = building.position
        cell_num = building.dic['cells_number']
        for i in range(pos_x - offset, pos_x + cell_num + offset):
            for j in range(pos_y - offset, pos_y + cell_num + offset):
                if i == pos_x and j == pos_y:
                    continue
                if not position_is_valid(i, j):
                    continue
                voisins_tuples.add((i, j))
        return voisins_tuples

    def get_prefets(self):
        prefets = []
        for building in self.prefecture_list:
            prefets += list(building.get_all_employees(real_object=True))
        """
        for walker in self.walkersOut:
            if isinstance(walker, walkers.Prefect):
                prefets.append(walker)
        """
        return prefets
    
    def identify_owner(self, sender_ip):
        for (ip,port),color in self.players:
                if ip == sender_ip:
                    return (ip, port)

    def include_incoming_packets(self, packets,update):
        layer_to_be_updated = set()
        for packet in packets:
            if packet.type == PacketTypes.Update:
                update_dict = decode_update_packets(packet)                
                for building_pos_to_remove in update_dict['removed']:
                    self.remove_element(building_pos_to_remove, from_packet=True)
                
                for building_pos_burning in update_dict['catchedfire']:
                    building = self.map.buildings_layer.get_cell(building_pos_burning[0], building_pos_burning[1])
                    building.isBurning = True
                    building.BurningTime = 0
                    building.risk_dico['fire'] = 100
                    building.functional = False

                    cases = self.map.buildings_layer.get_all_positions_of_element(building_pos_burning[0], building_pos_burning[1])
                    for i in cases:
                        self.map.buildings_layer.array[i[0]][i[1]].isBurning = True
                        update.catchedfire.append(i)

                for building_pos_collapsed in update_dict['collapsed']:
                    building = self.map.buildings_layer.get_cell(building_pos_collapsed[0], building_pos_collapsed[1])
                    building.isDestroyed = True
                    building.isBurning = False
                    building.risk_dico['collapse'] = 100

                    building.functional = False

                    cases = self.map.buildings_layer.get_all_positions_of_element(building_pos_burning[0], building_pos_burning[1])
                    for i in cases:
                        self.map.buildings_layer.array[i[0]][i[1]].isDestroyed = True
                        update.collapsed.append(i)
                # ---------------------------------------------------------
                # Evolution managment
                # We exchange evolution of dwelling that are suplly-updated by walkers
                # ---------------------------------------------------------
                is_one_priest_present = len(self.food_structures_list) != 0 and self.food_structures_list[0].is_functional()
                is_one_trader_present = len(self.temple_structures_list) != 0 and self.temple_structures_list[0].is_functional()
                active_updating_dwell_lvl_job = [is_one_priest_present, is_one_trader_present]
                if any(active_updating_dwell_lvl_job):
                    for building_pos_evolved in update_dict['has_evolved']:
                        building = self.map.buildings_layer.get_cell(building_pos_evolved[0], building_pos_evolved[1])
                        building.update_with_supply('temple', evolvable=True)
                        building.update_with_supply('food', evolvable=True)

            elif packet.type == PacketTypes.Walker_mov:
                for walker_mov_upd, ip in decode_walkers_movments_packets(packet=packet):
                    w_type, init_pos, dest_pos, target_pos = walker_mov_upd

                    walker_enterprise = walkers.reverse_convert_value_into_activity_field(w_type)
                    if not walker_enterprise:
                        continue
                    tmp = walker_enterprise + '_list'
                    structures_list = getattr(self, tmp)
                    # Get a walker owned by the sender_player who has the same job
                    sender = self.identify_owner(ip)
                    for building in structures_list:
                        if building.owner == sender:
                            # we have a valid building
                            # we teleport the walker
                            the_ultimate_walker = list(building.get_all_employees(real_object=True))[0]
                            the_ultimate_walker.init_pos = init_pos
                            the_ultimate_walker.dest_pos = None
                            the_ultimate_walker.offset_x, the_ultimate_walker.offset_y = 0, 0
                            the_ultimate_walker.compteur = 0
                            the_ultimate_walker.wait = False
                            the_ultimate_walker.current_path_to_follow = []
                            the_ultimate_walker.move_to_another_dwell(target_pos, walk_through=True)
          
            elif packet.type in [PacketTypes.Init,PacketTypes.Broacast_new_player,PacketTypes.Send_IP,PacketTypes.Ask_Broadcast,PacketTypes.Sauvegarde_ask]:
                Adress,port = decode_login_packets(packet)
                match packet.type:
                    case PacketTypes.Init:
                        self.players.append(((Adress,port),(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
                        echanger.send(Packet(packet.body,port,self.owner[0],Adress,packetType=PacketTypes.Send_IP))
                    case PacketTypes.Broacast_new_player:
                        ipList = [player[0] for player in self.players]
                        if (Adress,port) in ipList:
                            continue
                        self.players.append(((Adress,port),(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
                        echanger.send(Packet(struct.pack("IH", Packet.intAddressFromAdress(self.owner[0]),self.owner[1]),port,self.owner[0],Adress,packetType=PacketTypes.Send_IP))
                    case PacketTypes.Send_IP:
                        ipList = [player[0] for player in self.players]
                        if (Adress,port) in ipList:
                            continue
                        self.players.append(((Adress,port),(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
                        echanger.send(Packet(struct.pack("IH", Packet.intAddressFromAdress(self.owner[0]),self.owner[1]),port,self.owner[0],Adress,packetType=PacketTypes.Send_IP))
                    case PacketTypes.Ask_Broadcast:
                        echanger.send(Packet(packet.body,0,self.owner[0],"255.255.255.255",packetType=PacketTypes.Broacast_new_player))
                    case PacketTypes.Sauvegarde_ask:
                        saveLoad.save_game(self, "to-send")
                        p = Packet(b"", port, self.owner[0], Adress,PacketTypes.Sauvegarde_send)
                        echanger.send(p,True)
            elif packet.type in [PacketTypes.Ajouter,PacketTypes.Supprimer,PacketTypes.Ajout_Route,PacketTypes.Suppr_Route]:
                ponctual_data, ip_source = decode_ponctual_packets(packet)
                match packet.type:
                    case PacketTypes.Ajouter:
                        self.add_building(
                            ponctual_data[0][0], ponctual_data[0][1], dict_demon[ponctual_data[1]],from_packet=ip_source)
                        layer_to_be_updated.add("buildings")
                    case PacketTypes.Supprimer:
                        self.remove_element((ponctual_data[0], ponctual_data[1]))
                        layer_to_be_updated.add("buildings")
                        layer_to_be_updated.add("roads")
                    case PacketTypes.Ajout_Route:
                        self.add_road(
                            ponctual_data[0], ponctual_data[1],from_packet=ip_source)
                        layer_to_be_updated.add("roads")
                    case PacketTypes.Suppr_Route:
                        self.remove_element(
                            ponctual_data[0], ponctual_data[1])
        return layer_to_be_updated

    def send_update_packets(self, packets):
        for packet in packets:
            echanger.send(packet, True)

    def generateStat(self):
        stats = {}
        for player in self.players:
            stats[f"{player[0][0]}:{player[0][1]}"] = 0

        for building in self.buildinglist:
            txt = " ".join(building.dic["version"].split("_"))

            score = building_dico[txt].cost
            if (building.is_functional):   # chaque bat fonctionnel
                score += 10
            if (building.dic['version'] == "dwell"):   # si c'est une maison (car sinon pb avec prefecture)
                score += (building.structure_level) * 5  # niveau 1 (+5) ; niveau 2 (+10)
            else:
                score += 20  # si c'est un autre bat : +20
            if (building.isDestroyed or building.isBurning):      # -10pts par destruction
                score *= -1

            stats[f"{building.owner[0]}:{building.owner[1]}"] += score

        return stats
