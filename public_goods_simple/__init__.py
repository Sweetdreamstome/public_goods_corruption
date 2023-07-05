from otree.api import *



class C(BaseConstants):
    NAME_IN_URL = 'public_goods_simple'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)
    MULTIPLIER = 1.8
    FUNCIONARIO_ROLE = 'Funcionario'
    CIUDADANO1_ROLE = 'Ciudadano 1'
    CIUDADANO2_ROLE = 'Ciudadano 2'
    CIUDADANO3_ROLE = 'Ciudadano 3'
    #CIUDADANO4_ROLE = 'Ciudadano 4'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    iteration = models.IntegerField(initial=0)
    finished_sg = models.BooleanField(initial=False)


class Player(BasePlayer):
    iteration = models.IntegerField(initial=0)
    monto = models.IntegerField()
    monto_offer1 = models.IntegerField()
    monto_offer2 = models.IntegerField()
    monto_offer3 = models.IntegerField()
    monto_request1 = models.IntegerField()
    monto_request2 = models.IntegerField()
    monto_request3 = models.IntegerField()
    is_ready = models.BooleanField(initial=False)
    i_decided = models.BooleanField(initial=False)
    i_funcionario = models.BooleanField(initial = False)

    monto_fun1 = models.IntegerField()
    monto_fun2 = models.IntegerField()
    monto_fun3 = models.IntegerField()
    

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

# PAGES
class WaitToStart(WaitPage):
    pass
    #@staticmethod
    #def after_all_players_arrive(group: Group):
        # # make the first one
        # Game.create(group=group, iteration=group.iteration)

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
        my_id = player.id_in_group     
        role1 = player.get_others_in_group()[0].role
        role2 = player.get_others_in_group()[1].role
        role3 = player.get_others_in_group()[2].role
        other_id1 = player.get_others_in_group()[0].id_in_group
        other_id2 = player.get_others_in_group()[1].id_in_group
        other_id3 = player.get_others_in_group()[2].id_in_group

        if data['type'] == 'bien_publico':
            if 'monto' in data:
                try:
                    monto = int(data['monto'])
                except Exception:
                    print('Invalid', data)
                    return
                player.monto = monto
                player.i_decided = True
            
            if 'monto_fun1' in data:
                try:
                    monto_fun1 = int(data['monto_fun1'])
                except Exception:
                    print('Invalid', data)
                    return
                player.monto_fun1 = monto_fun1
                player.get_others_in_group()[0].monto_fun1 = monto_fun1
                player.get_others_in_group()[1].monto_fun1 = monto_fun1
                player.get_others_in_group()[2].monto_fun1 = monto_fun1

            if 'monto_fun2' in data:
                try:
                    monto_fun2 = int(data['monto_fun2'])
                except Exception:
                    print('Invalid', data)
                    return
                player.monto_fun2 = monto_fun2
                player.get_others_in_group()[0].monto_fun2 = monto_fun2
                player.get_others_in_group()[1].monto_fun2 = monto_fun2
                player.get_others_in_group()[2].monto_fun2 = monto_fun2

            if 'monto_fun3' in data:
                try:
                    monto_fun3 = int(data['monto_fun3'])
                except Exception:
                    print('Invalid', data)
                    return
                player.monto_fun3 = monto_fun3
                player.get_others_in_group()[0].monto_fun3 = monto_fun3
                player.get_others_in_group()[1].monto_fun3 = monto_fun3
                player.get_others_in_group()[2].monto_fun3 = monto_fun3

            if 'monto_fun1' and 'monto_fun2' and 'monto_fun3' in data:
                player.i_decided = True
                player.i_funcionario = True
        
        if data['type'] == 'offer':
            if 'monto_offer1' in data:
                try:
                    monto_offer1 = int(data['monto_offer1'])
                    player.monto_offer1 = monto_offer1
                except Exception:
                    print('Invalid', data)
            if 'monto_offer2' in data:
                try:
                    monto_offer2 = int(data['monto_offer2'])
                    player.monto_offer2 = monto_offer2
                except Exception:
                    print('Invalid', data)
            if 'monto_offer3' in data:
                try:
                    monto_offer3 = int(data['monto_offer3'])
                    player.monto_offer3 = monto_offer3
                except Exception:
                    print('Invalid',data)

        if data['type'] == 'request':
            if 'monto_request1' in data:
                try:
                    monto_request1 = int(data['monto_request1'])
                    player.monto_request1 = monto_request1
                except Exception:
                    print('Invalid', data)
            if 'monto_request2' in data:
                try:
                    monto_request2 = int(data['monto_request2'])
                    player.monto_request2 = monto_request2
                except Exception:
                    print('Invalid', data)
            if 'monto_request3' in data:
                try:
                    monto_request3 = int(data['monto_request3'])
                    player.monto_request3 = monto_request3
                except Exception:
                    print('Invalid', data)
            
        proposals = []
        montos = []
        montos_privados = []
        montos_funcionario = []

        if player.field_maybe_none('monto_fun1') and player.field_maybe_none('monto_fun2') and player.field_maybe_none('monto_fun3') is not None:
            montos_funcionario.append(player.monto_fun1)
            montos_funcionario.append(player.monto_fun2)
            montos_funcionario.append(player.monto_fun3)


        for p in {player, player.get_others_in_group()[0], player.get_others_in_group()[1], player.get_others_in_group()[2]}:
            monto = p.field_maybe_none('monto')
            if monto is not None:
                proposals.append([p.id_in_group, monto])
                montos.append(monto)

        if player.field_maybe_none('monto_offer1') is not None:
                montos_privados.append([role1, player.field_maybe_none('monto_offer1'), 'offer'])
        if player.field_maybe_none('monto_offer2') is not None:
                montos_privados.append([role2, player.field_maybe_none('monto_offer2'), 'offer'])
        if player.field_maybe_none('monto_offer3') is not None:
                montos_privados.append([role3, player.field_maybe_none('monto_offer3'), 'offer'])
        if player.field_maybe_none('monto_request1') is not None:
                montos_privados.append([role1, player.field_maybe_none('monto_request1'), 'request'])
        if player.field_maybe_none('monto_request2')  is  not None:
                montos_privados.append([role2, player.field_maybe_none('monto_request2'), 'request' ])
        if player.field_maybe_none('monto_request3')  is not None:
                montos_privados.append([role3, player.field_maybe_none('monto_request3'), 'request' ])

        if player.i_funcionario == True or player.get_others_in_group()[0].i_funcionario == True or player.get_others_in_group()[1].i_funcionario == True or player.get_others_in_group()[2].i_funcionario == True:
            if len(montos) == 3:
                print(my_id, 'is ready')
                player.is_ready = True
                print(proposals)
                return {my_id: dict(montos_privados = montos_privados, proposals=proposals, should_wait = False, show_results = True, montos_funcionario = montos_funcionario),
                        other_id1: dict(show_results = True, proposals=proposals, montos_funcionario = montos_funcionario),
                        other_id2: dict(show_results = True, proposals=proposals, montos_funcionario = montos_funcionario),
                        other_id3: dict(show_results = True, proposals=proposals, montos_funcionario = montos_funcionario),
                        }
            else:
                print(my_id, 'is not ready')   
                player.is_ready = False       
                return {my_id: dict(montos_privados= montos_privados, should_wait = player.i_decided and not player.is_ready, show_results= False, montos_funcionario = montos_funcionario)}
        else:
            if len(montos) == 3:
                print(my_id, 'is ready')
                player.is_ready = True
                print(proposals)
                return {my_id: dict(montos_privados = montos_privados, proposals=proposals, should_wait = False, show_results = True),
                        other_id1: dict(show_results = True, proposals=proposals),
                        other_id2: dict(show_results = True, proposals=proposals),
                        other_id3: dict(show_results = True, proposals=proposals),
                        }
            else:
                print(my_id, 'is not ready')   
                player.is_ready = False       
                return {my_id: dict(montos_privados= montos_privados, should_wait = player.i_decided and not player.is_ready, show_results= False)}


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
