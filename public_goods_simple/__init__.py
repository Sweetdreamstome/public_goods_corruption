from otree.api import *



class C(BaseConstants):
    NAME_IN_URL = 'public_goods_simple'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)
    MULTIPLIER = 1.8
    #FUNCIONARIO_ROLE = 'Funcionario'
    CIUDADANO1_ROLE = 'Ciudadano 1'
    CIUDADANO2_ROLE = 'Ciudadano 2'
    CIUDADANO3_ROLE = 'Ciudadano 3'
    CIUDADANO4_ROLE = 'Ciudadano 4'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    iteration = models.IntegerField(initial=0)
    finished_sg = models.BooleanField(initial=False)


class Player(BasePlayer):
    iteration = models.IntegerField(initial=0)
    monto = models.IntegerField()
    is_ready = models.BooleanField(initial=False)
    i_decided = models.BooleanField(initial=False)
    

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
        if 'monto' in data:
            try:
                monto = int(data['monto'])
            except Exception:
                print('Invalid', data)
                return
            player.monto = monto
        proposals = []
        montos = []
        for p in {player, player.get_others_in_group()[0], player.get_others_in_group()[1], player.get_others_in_group()[2]}:
            monto = p.field_maybe_none('monto')
            if monto is not None:
                proposals.append([p.id_in_group, monto])
                player.i_decided = True
                montos.append(monto)

        if len(montos) == 4:
            player.is_ready = True
            print(proposals)
            return {0: dict(proposals=proposals, should_wait = False, show_results= True)}

        else:
            player.is_ready = False
            return {my_id: dict(should_wait = player.i_decided and not player.is_ready, show_results= False)}
    

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
