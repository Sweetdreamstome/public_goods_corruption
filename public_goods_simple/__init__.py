from otree.api import *



class C(BaseConstants):
    NAME_IN_URL = 'public_goods_simple'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)
    MULTIPLIER = 1.8
    FUNCIONARIO_ROLE = 'Funcionario'
    CIUDADANO1_ROLE = 'Ciudadano 1'
    CIUDADANO2_ROLE = 'Ciudadano 2'
    CIUDADANO3_ROLE = 'Ciudadano 3'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    monto_asignado1 = models.IntegerField()
    monto_asignado2 = models.IntegerField()
    monto_asignado3 = models.IntegerField()
    monto_enviado= models.IntegerField()
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
                'label': 'Chat with {}'.format(other.chat_nickname())
            })
        return configs

# PAGES
class Bargain(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(other_role=player.get_others_in_group()[0].role)

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)

    @staticmethod
    def live_method(player: Player, data):

        group = player.group
        #[other] = player.get_others_in_group()

        if 'monto1' and 'monto2' and 'monto3' and 'monto4' in data:
            try:
                monto1 = int(data['monto1'])
                monto2 = int(data['monto2'])
                monto3 = int(data['monto3'])
                monto4 = int(data['monto4'])

            except Exception:
                print('Invalid message received', data)
                return
            if data['type'] == 'propose':
                player.monto_asignado1 = monto1
                player.monto_asignado2 = monto2
                player.monto_asignado3 = monto3
                player.monto_enviado = monto4

            proposals = []
            monto_asignado1 = player.field_maybe_none('monto1')
            monto_asignado2 = player.field_maybe_none('monto2')
            monto_asignado3 = player.field_maybe_none('monto3')
            monto_enviado = player.field_maybe_none('monto4')
            if monto_asignado1 is not None:
                proposals.append([player.id_in_group, monto_asignado1])
            elif monto_asignado2  is not None:
                proposals.append([player.id_in_group, monto_asignado2])
            elif monto_asignado3  is not None:
                proposals.append([player.id_in_group, monto_asignado3])
            elif monto_enviado is not None:
                proposals.append([player.id_in_group, monto_enviado])
            print(proposals)
            return {0: dict(proposals=proposals)}

    # @staticmethod
    # def error_message(player: Player, values):
    #     group = player.group
    #     if not group.is_finished:
    #         return "Game not finished yet"

    # @staticmethod
    # def is_displayed(player: Player):
    #     """Skip this page if a deal has already been made"""
    #     group = player.group
    #     deal_price = group.field_maybe_none('deal_price')
    #     return deal_price is None

class Results(Page):
    pass


page_sequence = [Bargain, Results]
