from otree.api import *



class C(BaseConstants):
    NAME_IN_URL = 'public_goods_simple'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 5
    ENDOWMENT = cu(100)
    MULTIPLIER = 1.8
    FUNCIONARIO_ROLE = 'Funcionario'
    CIUDADANO1_ROLE = 'Ciudadano 1'
    CIUDADANO2_ROLE = 'Ciudadano 2'
    CIUDADANO3_ROLE = 'Ciudadano 3'
    #CIUDADANO4_ROLE = 'Ciudadano 4'
    ciudadanos = 3
    funcionarios = 1
    decididos = ['i_decided' + str(x) for x in range(1, ciudadanos + 2)]
    siguiente_ronda = ['next_round' + str(x) for x in range(1, ciudadanos + 2)]
    montos_ciudadanos = ['monto' + str(x) for x in range(2, ciudadanos + 2)]
    montos_funcionarios = ['monto_fun' + str(x) for x in range(1, ciudadanos + 1)]
    montos_ofrecidos = []
    montos_pedidos = []
    for x in range(1, PLAYERS_PER_GROUP):
        for y in range(1, PLAYERS_PER_GROUP + 1):
            montos_ofrecidos.append('monto_offer' + str(y) + str(x))
    for x in range(1, PLAYERS_PER_GROUP):
        for y in range(1, PLAYERS_PER_GROUP + 1):
            montos_pedidos.append('monto_request' + str(y) + str(x))





class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    iteration = models.IntegerField(initial=0)
    finished_rondas = models.BooleanField(initial=False)

class Player(BasePlayer):
    iteration = models.IntegerField(initial=0)
    # monto = models.IntegerField()
    # monto_offer1 = models.IntegerField()
    # monto_offer2 = models.IntegerField()
    # monto_offer3 = models.IntegerField()
    # monto_request1 = models.IntegerField()
    # monto_request2 = models.IntegerField()
    # monto_request3 = models.IntegerField()
    is_ready = models.BooleanField(initial=False)
    i_funcionario = models.BooleanField(initial = False)

    # monto_fun1 = models.IntegerField()
    # monto_fun2 = models.IntegerField()
    # monto_fun3 = models.IntegerField()
    

    def chat_nickname(self):
        return '{}'.format(self.role)

    def chat_configs(self):
        configs = []
        for other in self.get_others_in_group():
            if other.id_in_group < self.id_in_group:
                lower_id, higher_id = other.id_in_group, self.id_in_group
            else:
                lower_id, higher_id = self.id_in_group, other.id_in_group
            configs.append({
                # make a name for the channel that is the same for all
                # channel members. That's why we order it (lower, higher)
                'channel': '{}-{}-{}'.format(self.group.id, lower_id, higher_id),
                'label': 'Chat con {}'.format(other.chat_nickname())
            })
        return configs

def custom_export(players):
    print('parece que si funciona')
#  Export an ExtraModel called "Trial"

    yield ['session', 'round_number', 'iteration', 'monto2', 'monto3', 'monto4', 'monto_fun1', 'monto_fun2', 'monto_fun3', 
               'monto_offer11', 'monto_offer12', 'monto_offer13', 'monto_offer21', 'monto_offer22', 'monto_offer23', 'monto_offer31', 'monto_offer32', 'monto_offer33', 'monto_offer41', 'monto_offer42', 'monto_offer43', 
               'monto_request11', 'monto_request12', 'monto_request13', 'monto_request21', 'monto_request22', 'monto_request23', 'monto_request31', 'monto_request32', 'monto_request33', 'monto_request41', 'monto_request42', 'monto_request43',
            ]

    # 'filter' without any args returns everything
    rondas = Ronda.filter()
    for ronda in rondas:
        group = ronda.group
        session = group.session
        yield [
                session.code, group.round_number, 
                ronda.iteration, 
                ronda.monto2, ronda.monto3, ronda.monto4,
                ronda.monto_fun1, ronda.monto_fun2, ronda.monto_fun3,
                ronda.monto_offer11, ronda.monto_offer12, ronda.monto_offer13, 
                ronda.monto_offer21, ronda.monto_offer22, ronda.monto_offer23,
                ronda.monto_offer31, ronda.monto_offer32, ronda.monto_offer33,
                ronda.monto_offer41, ronda.monto_offer42, ronda.monto_offer43,
                ronda.monto_request11, ronda.monto_request12, ronda.monto_request13,
                ronda.monto_request21, ronda.monto_request22, ronda.monto_request23,
                ronda.monto_request31, ronda.monto_request32, ronda.monto_request33,
                ronda.monto_request41, ronda.monto_request42, ronda.monto_request43,
            ]    

class Ronda(ExtraModel):
    group = models.Link(Group)
    player = models.Link(Player)
    iteration = models.IntegerField()

    # for monto in [Constants.montos_ciudadanos, Constants.montos_funcionarios, Constants.montos_ofrecidos, Constants.montos_pedidos]:
    #     locals()[monto] = models.IntegerField()
    # del monto

    for monto in C.montos_ciudadanos:
        locals()[monto] = models.IntegerField()
    del monto

    for monto in C.montos_funcionarios:
        locals()[monto] = models.IntegerField()
    del monto

    for monto in C.montos_ofrecidos:
        locals()[monto] = models.IntegerField()
    del monto

    for monto in C.montos_pedidos:
        locals()[monto] = models.IntegerField()
    del monto

    for string in C.decididos:
        locals()[string] = models.BooleanField(initial=False)
    del string

    for string in C.siguiente_ronda:
        locals()[string] = models.BooleanField(initial=False)
    del string

    has_results = models.BooleanField(initial=False)
    is_ready = models.BooleanField(initial=False)
    i_funcionario = models.BooleanField(initial = False)
    i_ciudadanos = models.BooleanField(initial = False)

# def to_dict(ronda: Ronda):
#     return dict(montos_ciudadanos=ronda.monto, montos_ofrecidos=[ronda.monto_offer1, ronda.monto_offer2, ronda.monto_offer3], montos_pedidos=[ronda.monto_request1, ronda.monto_request2, ronda.monto_request3], montos_funcionario=[ronda.monto_fun1, ronda.monto_fun2, ronda.monto_fun3 ] )

# PAGES
class WaitToStart(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        # make the first one
        Ronda.create(group=group, iteration=group.iteration)

class Bargain(Page):

    @staticmethod
    def vars_for_template(player: Player):
        return dict(role1 =player.get_others_in_group()[0].role,
                    role2 =player.get_others_in_group()[1].role,
                    role3 =player.get_others_in_group()[2].role, )

    @staticmethod 
    def js_vars(player: Player):
        return dict(my_id = player.id_in_group)
    
    @staticmethod
    def live_method(player:Player, data):   
        group = player.group
        my_id = player.id_in_group     
        role1 = player.get_others_in_group()[0].role
        role2 = player.get_others_in_group()[1].role
        role3 = player.get_others_in_group()[2].role
        other_id1 = player.get_others_in_group()[0].id_in_group
        other_id2 = player.get_others_in_group()[1].id_in_group
        other_id3 = player.get_others_in_group()[2].id_in_group

        if group.finished_rondas:
            return {my_id: dict(finished_rondas=True)}
        
        [ ronda ] = Ronda.filter(group=group, iteration=group.iteration)

        if data['type'] == 'finish_round':
            if 'next_round' in data:
                next_round = data['next_round']
                if my_id == 1:
                    ronda.next_round1 = next_round 
                elif my_id == 2:
                    ronda.next_round2 = next_round 
                elif my_id == 3:
                    ronda.next_round3 = next_round 
                elif my_id == 4:
                    ronda.next_round4 = next_round 

        if data['type'] == 'bien_publico':
            if 'monto' in data:
                try:
                    monto = int(data['monto'])
                except Exception: 
                    print('Invalid', data)
                    return
                #El 1 siempre es el funcionario, esta hardcodeado de esta manera
                #Esta harcodeado con el id a partir de ahora, se puede arreglar?
                if my_id == 2:
                    ronda.monto2 = monto
                    ronda.i_decided2 = True
                elif my_id == 3:
                    ronda.monto3 = monto
                    ronda.i_decided3 = True
                elif my_id == 4:
                    ronda.monto4 = monto
                    ronda.i_decided4 = True
  
            if 'monto_fun1' in data:
                try:
                    monto_fun1 = int(data['monto_fun1'])
                    ronda.monto_fun1 = monto_fun1
                except Exception:
                    print('Invalid', data)

            if 'monto_fun2' in data:
                try:
                    monto_fun2 = int(data['monto_fun2'])
                    ronda.monto_fun2 = monto_fun2
                except Exception:
                    print('Invalid', data)

            if 'monto_fun3' in data:
                try:
                    monto_fun3 = int(data['monto_fun3'])
                    ronda.monto_fun3 = monto_fun3
                except Exception:
                    print('Invalid', data)

        
        if data['type'] == 'offer':
            if 'monto_offer1' in data:
                try:
                    monto = int(data['monto_offer1'])
                    if my_id == 1:
                        ronda.monto_offer11 = monto
                    elif my_id == 2:
                        ronda.monto_offer21 = monto
                    elif my_id == 3:
                        ronda.monto_offer31 = monto
                    elif my_id == 4:
                        ronda.monto_offer41 = monto
                except Exception:
                    print('Invalid', data)
                

            if 'monto_offer2' in data:
                try:
                    monto = int(data['monto_offer2'])
                    if my_id == 1:
                        ronda.monto_offer12 = monto
                    elif my_id == 2:
                        ronda.monto_offer22 = monto
                    elif my_id == 3:
                        ronda.monto_offer32 = monto
                    elif my_id == 4:
                        ronda.monto_offer42 = monto
                except Exception:
                    print('Invalid', data)

            if 'monto_offer3' in data:
                try:
                    monto = int(data['monto_offer3'])
                    if my_id == 1:
                        ronda.monto_offer13 = monto
                    elif my_id == 2:
                        ronda.monto_offer23 = monto
                    elif my_id == 3:
                        ronda.monto_offer33 = monto
                    elif my_id == 4:
                        ronda.monto_offer43 = monto
                except Exception:
                    print('Invalid',data)

        if data['type'] == 'request':
            if 'monto_request1' in data:
                try:
                    monto = int(data['monto_request1'])
                    if my_id == 1:
                        ronda.monto_request11 = monto
                    elif my_id == 2:
                        ronda.monto_request21 = monto
                    elif my_id == 3:
                        ronda.monto_request31 = monto
                    elif my_id == 4:
                        ronda.monto_request41 = monto
                except Exception:
                    print('Invalid', data)

            if 'monto_request2' in data:
                try:
                    monto = int(data['monto_request2'])
                    if my_id == 1:
                        ronda.monto_request12 = monto
                    elif my_id == 2:
                        ronda.monto_request22 = monto
                    elif my_id == 3:
                        ronda.monto_request32 = monto
                    elif my_id == 4:
                        ronda.monto_request42 = monto
                except Exception:
                    print('Invalid', data)

            if 'monto_request3' in data:
                try:
                    monto = int(data['monto_request3'])
                    if my_id == 1:
                        ronda.monto_request13 = monto
                    elif my_id == 2:
                        ronda.monto_request23 = monto
                    elif my_id == 3:
                        ronda.monto_request33 = monto
                    elif my_id == 4:
                        ronda.monto_request43 = monto
                except Exception:
                    print('Invalid', data)
            
        proposals = []
        montos = []
        montos_privados = []
        montos_funcionario = []

        if 'monto_fun1' and 'monto_fun2' and 'monto_fun3' in data:
            ronda.i_decided1 = True
            #Por hardcoding del rol de funcionario
            ronda.i_funcionario = True

        if ronda.monto_fun1 and ronda.monto_fun2 and ronda.monto_fun3 is not None:
            montos_funcionario.append(ronda.monto_fun1)
            montos_funcionario.append(ronda.monto_fun2)
            montos_funcionario.append(ronda.monto_fun3)
            #Funcionario ya llenó todas sus partes

        if ronda.monto2 and ronda.monto3 and ronda.monto4 is not None:
            proposals.append([2, ronda.monto2])
            proposals.append([3, ronda.monto3])
            proposals.append([4, ronda.monto4])
            ronda.i_ciudadanos = True
            #is_ready para la izquierda
            print(proposals)
            print(my_id, 'is ready')

        # for p in {player, player.get_others_in_group()[0], player.get_others_in_group()[1], player.get_others_in_group()[2]}:
        #     monto = p.field_maybe_none('monto')
        #     if monto is not None:
        #         proposals.append([p.id_in_group, monto])
        #         montos.append(monto)

        if my_id == 1:
            if ronda.monto_offer11 is not None:
                 montos_privados.append([role1, ronda.monto_offer11, 'offer'])
            if ronda.monto_offer12 is not None:
                 montos_privados.append([role2, ronda.monto_offer12, 'offer'])
            if ronda.monto_offer13 is not None:
                 montos_privados.append([role3, ronda.monto_offer13, 'offer'])                 
            if ronda.monto_request11 is not None:
                 montos_privados.append([role1, ronda.monto_request11, 'request'])
            if ronda.monto_request12 is not None:
                 montos_privados.append([role2, ronda.monto_request12, 'request'])
            if ronda.monto_request13 is not None:
                 montos_privados.append([role3, ronda.monto_request13, 'request'])

        elif my_id == 2:
            if ronda.monto_offer21 is not None:
                 montos_privados.append([role1, ronda.monto_offer21, 'offer'])
            if ronda.monto_offer22 is not None:
                 montos_privados.append([role2, ronda.monto_offer22, 'offer'])
            if ronda.monto_offer23 is not None:
                 montos_privados.append([role3, ronda.monto_offer23, 'offer'])                 
            if ronda.monto_request21 is not None:
                 montos_privados.append([role1, ronda.monto_request21, 'request'])
            if ronda.monto_request22 is not None:
                 montos_privados.append([role2, ronda.monto_request22, 'request'])
            if ronda.monto_request23 is not None:
                 montos_privados.append([role3, ronda.monto_request23, 'request'])

        elif my_id == 3:
            if ronda.monto_offer31 is not None:
                 montos_privados.append([role1, ronda.monto_offer31, 'offer'])
            if ronda.monto_offer32 is not None:
                 montos_privados.append([role2, ronda.monto_offer32, 'offer'])
            if ronda.monto_offer33 is not None:
                 montos_privados.append([role3, ronda.monto_offer33, 'offer'])                 
            if ronda.monto_request31 is not None:
                 montos_privados.append([role1, ronda.monto_request31, 'request'])
            if ronda.monto_request32 is not None:
                 montos_privados.append([role2, ronda.monto_request32, 'request'])
            if ronda.monto_request33 is not None:
                 montos_privados.append([role3, ronda.monto_request33, 'request'])

        elif my_id == 4:
            if ronda.monto_offer41 is not None:
                 montos_privados.append([role1, ronda.monto_offer41, 'offer'])
            if ronda.monto_offer42 is not None:
                 montos_privados.append([role2, ronda.monto_offer42, 'offer'])
            if ronda.monto_offer43 is not None:
                 montos_privados.append([role3, ronda.monto_offer43, 'offer'])                 
            if ronda.monto_request41 is not None:
                 montos_privados.append([role1, ronda.monto_request41, 'request'])
            if ronda.monto_request42 is not None:
                 montos_privados.append([role2, ronda.monto_request42, 'request'])
            if ronda.monto_request43 is not None:
                 montos_privados.append([role3, ronda.monto_request43, 'request'])

        # if player.field_maybe_none('monto_offer1') is not None:
        #         montos_privados.append([role1, player.field_maybe_none('monto_offer1'), 'offer'])
        # if player.field_maybe_none('monto_offer2') is not None:
        #         montos_privados.append([role2, player.field_maybe_none('monto_offer2'), 'offer'])
        # if player.field_maybe_none('monto_offer3') is not None:
        #         montos_privados.append([role3, player.field_maybe_none('monto_offer3'), 'offer'])
        # if player.field_maybe_none('monto_request1') is not None:
        #         montos_privados.append([role1, player.field_maybe_none('monto_request1'), 'request'])
        # if player.field_maybe_none('monto_request2')  is  not None:
        #         montos_privados.append([role2, player.field_maybe_none('monto_request2'), 'request' ])
        # if player.field_maybe_none('monto_request3')  is not None:
        #         montos_privados.append([role3, player.field_maybe_none('monto_request3'), 'request' ])
        is_done = False

        if ronda.next_round1 and ronda.next_round2 and ronda.next_round3 and ronda.next_round4:
            is_done = True

        if is_done:
            #game.has_results = True
            group.iteration += 1
            Ronda.create(group=group, iteration=group.iteration)
            return {
                0: dict(should_wait=False, iteration=group.iteration)
            }
        if ronda.next_round1:
            return{my_id: dict(montos_privados = montos_privados, proposals = proposals, should_wait = False, show_results = False, wait_ronda = True, montos_funcionario = montos_funcionario)
            }
        elif ronda.next_round2:
            return{my_id: dict(montos_privados = montos_privados, proposals = proposals, should_wait = False, show_results = False, wait_ronda = True, montos_funcionario = montos_funcionario)
            }      
        elif ronda.next_round3:
            return{my_id: dict(montos_privados = montos_privados, proposals = proposals, should_wait = False, show_results = False, wait_ronda = True, montos_funcionario = montos_funcionario)
            }    
        elif ronda.next_round4:
            return{my_id: dict(montos_privados = montos_privados, proposals = proposals, should_wait = False, show_results = False, wait_ronda = True, montos_funcionario = montos_funcionario)
            }

        if ronda.i_decided1 and ronda.i_decided2 and ronda.i_decided3 and ronda.i_decided4:
            return {my_id: dict(montos_privados = montos_privados, proposals = proposals, should_wait = False, show_results = True, montos_funcionario = montos_funcionario),
                    other_id1: dict(show_results= True, proposals = proposals, montos_funcionario = montos_funcionario),
                    other_id2: dict(show_results= True, proposals = proposals, montos_funcionario = montos_funcionario),
                    other_id3: dict(show_results= True, proposals = proposals, montos_funcionario = montos_funcionario),
            }
        else:
            if my_id == 1 and ronda.i_decided1:
                return { my_id: dict(montos_privados = montos_privados, proposals= proposals, should_wait = True, show_results = False, montos_funcionario = montos_funcionario),}
            elif my_id == 2 and ronda.i_decided2:
                return { my_id: dict(montos_privados = montos_privados, proposals= proposals, should_wait = True, show_results = False, montos_funcionario = montos_funcionario),}
            elif my_id == 3 and ronda.i_decided3:
                return { my_id: dict(montos_privados = montos_privados, proposals= proposals, should_wait = True, show_results = False, montos_funcionario = montos_funcionario),}
            elif my_id == 4 and ronda.i_decided4:
                return { my_id: dict(montos_privados = montos_privados, proposals= proposals, should_wait = True, show_results = False, montos_funcionario = montos_funcionario),}
            else:
                return { my_id: dict(montos_privados = montos_privados, should_wait = False, show_results = False, montos_funcionario = montos_funcionario)}
        
        
    
        
        # if player.i_funcionario == True or player.get_others_in_group()[0].i_funcionario == True or player.get_others_in_group()[1].i_funcionario == True or player.get_others_in_group()[2].i_funcionario == True:
        #     if len(montos) == 3:
        #         print(my_id, 'is ready')
        #         player.is_ready = True
        #         print(proposals)
        #         return {my_id: dict(montos_privados = montos_privados, proposals=proposals, should_wait = False, show_results = True, montos_funcionario = montos_funcionario),
        #                 other_id1: dict(show_results = True, proposals=proposals, montos_funcionario = montos_funcionario),
        #                 other_id2: dict(show_results = True, proposals=proposals, montos_funcionario = montos_funcionario),
        #                 other_id3: dict(show_results = True, proposals=proposals, montos_funcionario = montos_funcionario),
        #                 }
        #     else:
        #         print(my_id, 'is not ready')   
        #         player.is_ready = False       
        #         return {my_id: dict(montos_privados= montos_privados, should_wait = player.i_decided and not player.is_ready, show_results= False, montos_funcionario = montos_funcionario)}
        # else:
        #     if len(montos) == 3:
        #         print(my_id, 'is ready')
        #         player.is_ready = True
        #         print(proposals)
        #         return {my_id: dict(montos_privados = montos_privados, proposals=proposals, should_wait = False, show_results = True),
        #                 other_id1: dict(show_results = True, proposals=proposals),
        #                 other_id2: dict(show_results = True, proposals=proposals),
        #                 other_id3: dict(show_results = True, proposals=proposals),
        #                 }
        #     else:
        #         print(my_id, 'is not ready')   
        #         player.is_ready = False       
        #         return {my_id: dict(montos_privados= montos_privados, should_wait = player.i_decided and not player.is_ready, show_results= False)}


    # @staticmethod
    # def error_message(player: Player, monto):
    #     monto= player.monto
    #     group = player.group
    #     if monto > 500:
    #         return 'Tiene que ser un valor menor a 500'

    # @staticmethod
    # def is_displayed(player: Player):
    #     """Skip this page if a deal has already been made"""
    #     group = player.group
    #     deal_price = group.field_maybe_none('deal_price')
    #     return deal_price is None

class Results(Page):
    pass

class End(Page):
    pass



page_sequence = [WaitToStart, Bargain, End]
