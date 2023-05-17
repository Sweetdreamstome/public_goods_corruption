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
        [other] = player.get_others_in_group()

        if 'monto1' & 'monto2' & 'monto3' in data:
            try:
                monto1 = int(data['monto1'])
                monto2 = int(data['monto2'])
                monto3 = int(data['monto3'])
            except Exception:
                print('Invalid message received', data)
                return
            if data['type'] == 'propose':
                player.monto_asignado1 = monto1
                player.monto_asignado2 = monto2
                player.monto_asignado3 = monto3

        # proposals = []
        # for p in [player, other]:
        #     amount_proposed = p.field_maybe_none('amount_proposed')
        #     if amount_proposed is not None:
        #         proposals.append([p.id_in_group, amount_proposed])
        # return {0: dict(proposals=proposals)}

    @staticmethod
    def error_message(player: Player, values):
        group = player.group
        if not group.is_finished:
            return "Game not finished yet"

    # @staticmethod
    # def is_displayed(player: Player):
    #     """Skip this page if a deal has already been made"""
    #     group = player.group
    #     deal_price = group.field_maybe_none('deal_price')
    #     return deal_price is None

class Results(Page):
    pass


page_sequence = [Bargain, Results]
