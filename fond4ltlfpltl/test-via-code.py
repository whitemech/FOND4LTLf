from fond4ltlfpltl.core import execute


def main():
    formula_1 = "F(vehicleat_l31)"
    in_domain = open("../tests/dom.pddl").read()
    in_problem = open("../tests/prob.pddl").read()

    domain_prime, problem_prime = execute(in_domain, in_problem, formula_1)
    domain_second, problem_second = execute(in_domain, in_problem, formula_1)
    # print(str(problem_prime) == str(problem_second))

    # print("======== Domain File ========\n{}\n\n======== Problem File ========\n{}".format(domain_prime, problem_prime))
    # print("======== Domain File ========\n{}\n\n======== Problem File ========\n{}".format(domain_second,
    #                                                                                         problem_second))

    formula_2 = "vehicleat_l31 & O(vehicleat_12)"

    domain_prime, problem_prime = execute(in_domain, in_problem, formula_2)
    domain_second, problem_second = execute(in_domain, in_problem, formula_2)

    print(
        "======== Domain File ========\n{}\n\n======== Problem File ========\n{}".format(
            domain_prime, problem_prime
        )
    )
    print(
        "======== Domain File ========\n{}\n\n======== Problem File ========\n{}".format(
            domain_second, problem_second
        )
    )


if __name__ == "__main__":
    main()
