"""
Implement violation-aware Bayesian optimizer.
"""
import numpy as np
from .base_optimizer import BaseEGO


class CONFIGOpt(BaseEGO):

    def __init__(self, opt_problem, lcb2_config):
        # optimization problem and measurement noise
        super().__init__(opt_problem, lcb2_config)

        # Pr(cost <= beta * budget) >= 1 - \epsilon
        if 'beta_func' in lcb2_config.keys():
            self.beta_func = lcb2_config['beta_func']
        else:
            self.beta_func = lambda t: 3

        if 'total_eval_num' not in lcb2_config.keys():
            lcb2_config['total_eval_num'] = 100

        self.INF = 1e10
        self.num_eps = 1e-10   # epsilon for numerical value
        self.t = 0
        self.total_eval_num = lcb2_config['total_eval_num']

    def get_acquisition(self, prob_eps=None):
        obj_mean, obj_var = self.gp_obj.predict(self.parameter_set)
        obj_mean = obj_mean.squeeze()
        obj_var = obj_var.squeeze()

        constrain_mean_list = []
        constrain_var_list = []
        for i in range(self.opt_problem.num_constrs):
            mean, var = self.gp_constr_list[i].predict(self.parameter_set)
            constrain_mean_list.append(np.squeeze(mean))
            constrain_var_list.append(np.squeeze(var))

        constrain_mean_arr = np.array(constrain_mean_list).T
        constrain_var_arr = np.array(constrain_var_list).T

        beta = self.beta_func(self.t)
        obj_lcb = obj_mean - beta * np.sqrt(obj_var)

        constrain_lcb_arr = constrain_mean_arr - \
            beta * np.sqrt(constrain_var_arr)

        lcb_feasible = np.prod(1.0 * (constrain_lcb_arr <= 0.0), axis=1)
        return obj_lcb, lcb_feasible

    def addObjectiveSample(self, x_to_add, obj_to_add):
        # add a scalar objective
        if type(x_to_add) == list:
            x_to_add = np.array(x_to_add)
        if x_to_add.ndim == 1:
            x_to_add = np.expand_dims(x_to_add, axis=0)

        obj_to_add = np.atleast_2d(obj_to_add)
        # Add this to the GP model
        prev_X = self.gp_obj.X
        prev_obj = self.gp_obj.Y

        new_X = np.vstack([prev_X, x_to_add])
        new_obj = np.vstack([prev_obj, obj_to_add])
        self.gp_obj.set_XY(new_X, new_obj)

    def addConstraintSample(self, x_to_add, constraint_to_add):
        # add a list of constraint or a constraint
        if isinstance(constraint_to_add, np.ndarray) or \
                isinstance(constraint_to_add, list):
            pass
        else:
            constraint_to_add = [constraint_to_add]

        if type(x_to_add) == list:
            x_to_add = np.array(x_to_add)
        if x_to_add.ndim == 1:
            x_to_add = np.expand_dims(x_to_add, axis=0)

        for k in range(self.opt_problem.num_constrs):
            prev_X = self.gp_constr_list[k].X
            prev_Y = self.gp_constr_list[k].Y

            y_to_add = np.atleast_2d(constraint_to_add[k])

            new_X = np.vstack([prev_X, x_to_add])
            new_Y = np.vstack([prev_Y, y_to_add])
            self.gp_constr_list[k].set_XY(new_X, new_Y)

    def optimize(self):
        obj_lcb, lcb_feasible = self.get_acquisition()
        next_point_id = np.argmin(obj_lcb + (1.0-lcb_feasible) * self.INF)
        next_point = self.parameter_set[next_point_id]
        return next_point
