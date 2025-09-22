
import sys
from labs.lab3.satFileReaders import readInstance, readSolution


def main():
    if len(sys.argv) != 3:
        usage()

    cnf_path = sys.argv[1]
    sol_path = sys.argv[2]

    try:
        variables, clauses = readInstance(cnf_path)
    except Exception as e:
        print(f"Error reading CNF instance '{cnf_path}': {e}")
        sys.exit(2)

    try:
        assignment, _ = readSolution(sol_path)
    except Exception as e:
        print(f"Error reading solution file '{sol_path}': {e}")
        sys.exit(2)

    print(assignment)

def usage():
    print("Usage: python SAT <cnf_instance> <solution_file>")
    sys.exit(1)





if __name__ == "__main__":
    main()
