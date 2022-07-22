from pyomo.environ import * 

model = AbstractModel()

## Define sets
model.Refineries = Set()
model.Depots = Set()

## Define parameters
model.refinery = Param(model.Refineries)
model.depot = Param(model.Depots)
model.costs = Param(model.Refineries, model.Depots)

## Define variables
model.flow = Var(model.Refineries, model.Depots, within = NonNegativeReals)

## Define Objective Function
def costRule(model):
   return sum(
       model.costs[n,i] * model.flow[n,i]
       for n in model.Refineries
       for i in model.Depots
    )
model.SolverResult=Objective(rule=costRule)

## Satisfy demands
def minDemandRule(model,bar):
    return sum(model.flow[i, bar] for i in model.Refineries) >= model.depot[bar]
model.depotConstraint = Constraint(model.Depots, rule=minDemandRule)

## Satisfy supplies
def maxSupplyRule(model,warehouse):
    return sum(model.flow[warehouse, j] for j in model.Depots) <= model.refinery[warehouse]
model.refineryConstraint = Constraint(model.Refineries, rule=maxSupplyRule)
