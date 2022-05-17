distributions = {'Akkadian': {'OSV': 0.2634146341463415, 'SOV': 0.6390243902439025, 'SVO': 0.08780487804878048, 'OVS': 0.00975609756097561},
'Amharic': {'OVS': 0.4312896405919662, 'VSO': 0.08879492600422834, 'OSV': 0.1226215644820296, 'SOV': 0.30021141649048627, 'SVO': 0.052854122621564484, 'VOS': 0.004228329809725159},
'Arabic': {'VSO': 0.5356336665591744, 'VOS': 0.22683005482102547, 'OVS': 0.0634633989035795, 'SVO': 0.16788132860367624, 'SOV': 0.0029667849080941633, 'OSV': 0.0032247662044501773},
'Bambara': {'SOV': 1.0},
'Basque': {'OVS': 0.17367332873880081, 'SOV': 0.5582356995175741, 'SVO': 0.21157822191592005, 'OSV': 0.03170227429359063, 'VOS': 0.011026878015161957, 'VSO': 0.013783597518952447},
'Buryat': {'SOV': 0.8805970149253731, 'SVO': 0.029850746268656716, 'OSV': 0.08955223880597014},
'Chinese': {'SVO': 0.9992673992673993, 'SOV': 0.0007326007326007326},
'Chukchi': {'VSO': 0.01694915254237288, 'OVS': 0.11864406779661017, 'SOV': 0.3728813559322034, 'OSV': 0.1694915254237288, 'SVO': 0.3220338983050847},
'Coptic': {'SVO': 1.0},
'Estonian': {'SVO': 0.550125313283208, 'SOV': 0.12364243943191311, 'VSO': 0.14466722361459203, 'OVS': 0.09273182957393483, 'OSV': 0.04831523252575884, 'VOS': 0.04051796157059315},
'German': {'VSO': 0.1458152563978961, 'SOV': 0.46952898201411875, 'OSV': 0.07333611852042292, 'OVS': 0.04518430439952437, 'SVO': 0.2465747554927103, 'VOS': 0.019560583175327526},
'Guarani': {'SOV': 0.3918918918918919, 'SVO': 0.5405405405405406, 'OSV': 0.05405405405405406, 'OVS': 0.013513513513513514},
'Hungarian': {'OSV': 0.13414634146341464, 'SVO': 0.4292682926829268, 'SOV': 0.2731707317073171, 'OVS': 0.10975609756097561, 'VOS': 0.03902439024390244, 'VSO': 0.014634146341463415},
'Indonesian': {'SVO': 0.9792429792429792, 'OSV': 0.019943019943019943, 'VOS': 0.000814000814000814},
'Irish': {'VSO': 0.7343311506080449, 'OVS': 0.09915809167446211, 'SVO': 0.1646398503274088, 'VOS': 0.0009354536950420954, 'OSV': 0.0009354536950420954},
'Japanese': {'SOV': 0.9523916967509025, 'OSV': 0.04760830324909747},
'Kiche': {'VOS': 0.3153846153846154, 'SVO': 0.6, 'OVS': 0.07692307692307693, 'SOV': 0.007692307692307693},
'Komi': {'SVO': 0.5784313725490197, 'SOV': 0.21568627450980393, 'OVS': 0.08823529411764706, 'OSV': 0.0784313725490196, 'VSO': 0.00980392156862745, 'VOS': 0.029411764705882353},
'Korean': {'SOV': 0.9655688622754491, 'OSV': 0.0344311377245509},
'Naija': {'SVO': 0.9997313272434175, 'SOV': 0.00026867275658248256},
'Persian': {'SOV': 0.9722587239012994, 'OSV': 0.025405168637757335, 'OVS': 0.0007300335815447511, 'SVO': 0.0016060738793984522},
'Russian': {'OVS': 0.08928786600795277, 'SVO': 0.7455717556332088, 'SOV': 0.06639354139052898, 'VSO': 0.010965176527292444, 'OSV': 0.06741776117604531, 'VOS': 0.020363899264971685},
'Telugu': {'SOV': 0.7990654205607477, 'OSV': 0.18691588785046728, 'SVO': 0.009345794392523364, 'OVS': 0.004672897196261682},
'Thai': {'SVO': 0.9571183533447685, 'OSV': 0.04288164665523156},
'Turkish': {'SOV': 0.9797919762258543, 'OVS': 0.0008915304606240713, 'OSV': 0.017533432392273403, 'SVO': 0.0017830609212481426},
'Vietnamese': {'SVO': 0.9568965517241379, 'SOV': 0.005172413793103448, 'OSV': 0.03793103448275862},
'Wolof': {'SVO': 0.613160518444666, 'SOV': 0.16350947158524426, 'OSV': 0.22333000997008973},
'Xibe': {'SOV': 0.9458333333333333, 'OSV': 0.05416666666666667},
'Yoruba': {'SVO': 0.9265175718849841, 'OSV': 0.051118210862619806, 'SOV': 0.019169329073482427, 'VSO': 0.003194888178913738}}
from tabulate import tabulate
def tabulator(distributions):
    table = []
    for lang in distributions.keys():
        line = []
        line.append(lang)
        for order in ['SOV', 'SVO', 'VSO', 'VOS', 'OSV', 'OVS']:
            if order not in distributions[lang].keys():
                line.append(' ')
            else:
                line.append(round((distributions[lang][order]),4))
        table.append(line)
    print(tabulate(table, ['SOV', 'SVO', 'VSO', 'VOS', 'OSV', 'OVS'], tablefmt="latex"))

tabulator(distributions)
        