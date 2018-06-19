import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

temperatura = ctrl.Antecedent(np.arange(100, 500, 1), 'temperatura')
pressao = ctrl.Antecedent(np.arange(4, 12, 1), 'pressao')
acelerador = ctrl.Consequent(np.arange(0, 100, 1), 'acelerador')

temperatura['baixa'] = fuzz.trapmf(temperatura.universe, [100, 100, 200, 300])
temperatura['media'] = fuzz.trimf(temperatura.universe, [200, 300, 400])
temperatura['alta'] = fuzz.trapmf(temperatura.universe, [300, 400, 500, 500])
temperatura.view()

pressao['baixa'] = fuzz.trapmf(pressao.universe, [4, 4, 6, 8])
pressao['media'] = fuzz.trimf(pressao.universe, [6, 8, 10])
pressao['alta'] = fuzz.trapmf(pressao.universe, [8, 10, 12, 12])
pressao.view()

acelerador['min'] = fuzz.trapmf(acelerador.universe, [0, 0, 25, 50])
acelerador['0'] = fuzz.trimf(acelerador.universe, [25, 50, 75])
acelerador['max'] = fuzz.trapmf(acelerador.universe, [50, 75, 100, 100])
acelerador.view()


rule1 = ctrl.Rule(temperatura['media'] & pressao['media'], acelerador['0'])
rule2 = ctrl.Rule(temperatura['alta'] & pressao['alta'], acelerador['max'])
rule3 = ctrl.Rule(temperatura['media'] & pressao['media'], acelerador['0'])
rule4 = ctrl.Rule(temperatura['alta'] & pressao['alta'], acelerador['max'])

acelerador_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
acel = ctrl.ControlSystemSimulation(acelerador_ctrl)

acel.input['temperatura'] = 350
acel.input['pressao'] = 9

# Crunch the numbers
acel.compute()
acelerador.view(sim=acel)
print(acel.output['acelerador'])
plt.show()