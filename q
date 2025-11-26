warning: in the working copy of 'assignments/assignment2/Barrett_R00029480_MH2.py', LF will be replaced by CRLF the next time Git touches it
[1mdiff --git a/assignments/assignment2/Barrett_R00029480_MH2.py b/assignments/assignment2/Barrett_R00029480_MH2.py[m
[1mindex e10ece2..928801d 100644[m
[1m--- a/assignments/assignment2/Barrett_R00029480_MH2.py[m
[1m+++ b/assignments/assignment2/Barrett_R00029480_MH2.py[m
[36m@@ -276,7 +276,21 @@[m [mclass GSAT_solver:[m
         (c) Otherwise randomly choose unsat clause and choose variable with maximum net gain, breaking ties randomly[m
         Advice: adapt WalkSAT code from selectWalkSATvar[m
         '''[m
[31m-        pass[m
[32m+[m[32m        # Positive gain is the number of variables that are unsat that will go sat[m
[32m+[m[32m        # negatice gain is the number of variables that are sat that will go unsat[m
[32m+[m[32m        # next gain is the sum of unsat  - the sum of unsat when we flip a variable.[m
[32m+[m[32m        zero_damage_variables = self._get_zero_damage_variables()[m
[32m+[m[32m        if len(zero_damage_variables) > 0:[m
[32m+[m[32m            return np.random.choice(zero_damage_variables)[m
[32m+[m
[32m+[m[32m        random_clause = self._select_random_unsat_clause()[m
[32m+[m
[32m+[m[32m        if random.random() < self.wp:[m
[32m+[m[32m            # TODO: is this all clauses? it says at least one.[m
[32m+[m[32m            unsat_variables = self._get_all_variables_in_unsat_clauses()[m
[32m+[m[32m            return np.random.choice(unsat_variables)[m
[32m+[m
[32m+[m[32m        return self._select_max_gain_variable_from_clause(random_clause)[m
 [m
     def selectGrimesHSATvar(self):[m
         '''[m
[36m@@ -288,8 +302,55 @@[m [mclass GSAT_solver:[m
         (c) Otherwise randomly choose unsat clause and choose variable with maximum net gain, breaking ties randomly[m
         Advice: adapt WalkSAT code from selectWalkSATvar[m
         '''[m
[31m-        pass[m
[32m+[m[32m        zero_damage_variables = self._get_zero_damage_variables()[m
[32m+[m[32m        if len(zero_damage_variables) > 0:[m
[32m+[m[32m            return np.random.choice(zero_damage_variables)[m
 [m
[32m+[m[32m        if random.random() < self.wp:[m
[32m+[m[32m            unsat_variables = self._get_all_variables_in_unsat_clauses()[m
[32m+[m[32m            return unsat_variables[np.where(self.lastFlip[unsat_variables] == np.amin(self.lastFlip[unsat_variables]))[0]][0][m
[32m+[m
[32m+[m[32m        random_unsat_clause = self._select_random_unsat_clause()[m
[32m+[m[32m        return self._select_max_gain_variable_from_clause(random_unsat_clause)[m
[32m+[m
[32m+[m
[32m+[m[32m    def _get_all_variables_in_unsat_clauses(self):[m
[32m+[m[32m        """Returns all variables involved in at least one unsatisfied clause."""[m
[32m+[m[32m        variables = set()[m
[32m+[m[32m        for clause_index in self.unsat_clauses:[m
[32m+[m[32m            for literal in self.clauses[clause_index]:[m
[32m+[m[32m                variables.add(abs(literal))[m
[32m+[m[32m        return np.array(list(variables))[m
[32m+[m
[32m+[m[32m    def _select_random_unsat_clause(self):[m
[32m+[m[32m        """Select a random unsatisfied clause."""[m
[32m+[m[32m        return random.choice(tuple(self.unsat_clauses))[m
[32m+[m
[32m+[m[32m    def _select_max_gain_variable_from_clause(self, clause_index):[m
[32m+[m[32m        """[m
[32m+[m[32m        Select a variable with maximum net gain from a clause.[m
[32m+[m[32m        Break ties randomly.[m
[32m+[m[32m        """[m
[32m+[m[32m        variables = self._get_variables_from_clause(clause_index)[m
[32m+[m[32m        net_gains = self._calculate_gains(variables)[m
[32m+[m[32m        gains = self._get_gains_array(net_gains)[m
[32m+[m[32m        return variables[np.random.choice(gains)][m
[32m+[m
[32m+[m[32m    def _get_variables_from_clause(self, clause_index):[m
[32m+[m[32m        """Get variables from a clause"""[m
[32m+[m[32m        return [abs(lit) for lit in self.clauses[clause_index]][m
[32m+[m
[32m+[m[32m    def _calculate_gains(self, variables):[m
[32m+[m[32m        """Calculates gain """[m
[32m+[m[32m        return np.array([self.makecounts[var] - self.breakcounts[var] for var in variables])[m
[32m+[m
[32m+[m[32m    def _get_gains_array(self, gains):[m
[32m+[m[32m        """Returns an array of indices of maximum gain."""[m
[32m+[m[32m        return np.where(gains == np.amax(gains))[0][m
[32m+[m
[32m+[m[32m    def _get_zero_damage_variables(self):[m
[32m+[m[32m        """Returns variables with positive gain and zero damage."""[m
[32m+[m[32m        return np.where((self.makecounts > 0) & (self.breakcounts == 0))[0][m
         [m
     def solve(self):[m
         self.restarts = 0[m
