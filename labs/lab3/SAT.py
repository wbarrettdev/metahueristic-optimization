
import sys
from typing import Any

from numpy.f2py.auxfuncs import throw_error

from labs.lab3.satFileReaders import readInstance, readSolution

def load_solution(solution) -> dict[Any, Any]:
    try:
        return readSolution(solution)
    except Exception as e:
        print(f"Error reading solution file '{solution}': {e}")
        sys.exit(2)


def load_instance(instance) -> list[Any]:
    try:
        return readInstance(instance)
    except Exception as e:
        print(f"Error reading CNF instance '{instance}': {e}")
        sys.exit(2)


def is_solution(assignment: dict[Any, Any], clauses: list[Any], cost: int) -> int:
    for clause in clauses:
        satisfied = False
        for value in clause:
            polarity = True
            if value == 0:
                throw_error("Invalid clause")
            if value < 0:
                polarity = False
                value *= -1

            check_assignment = assignment[value]
            if check_assignment == polarity:
                satisfied = True
        if satisfied != True:
            cost -= -1
    return cost


def usage():
    print("Usage: python SAT <cnf_instance> <solution_file>")
    sys.exit(1)





if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()

    cnf_path = sys.argv[1]
    sol_path = sys.argv[2]

    variables, clauses = load_instance(cnf_path)
    assignment, _ = readSolution(sol_path)

    cost = is_solution(assignment, clauses, len(clauses))
    if cost == len(clauses):
        print(f"SOLUTION {cnf_path} {sol_path}" )
    else:
        print(f"Cost {cnf_path} {sol_path} {cost}")
        print("Not the Solution")



# uf20-01.cnf -> sols/a_sol.txt
# uf20-02.cnf -> sols/d_sol.txt
# uf20-03.cnf -> sols/t_sol.txt
# uf20-04.cnf -> sols/ce_sol.txt
# uf20-05.cnf -> sols/cu_sol.txt
# uf20-06.cnf -> sols/sa_sol.txt
# uf20-07.cnf -> sols/sb_sol.txt
# uf20-08.cnf -> sols/o_sol.txt
# uf20-09.cnf -> sols/n_sol.txt