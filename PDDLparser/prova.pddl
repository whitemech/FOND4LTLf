(define (domain blocks)
	(:requirements :strips :typing :equality :adl)
	(:types block)
	(:predicates
		(on ?x - block ?y - block)
		(ontable ?x - block)
		(clear ?x - block)
		(handempty)
		(holding ?x - block)
	)

	(:action pick-up
		:parameters (?x - block)
		:precondition (and
			(clear ?x)
			(ontable ?x)
			(handempty)
		)
		:effect (and
			(not (ontable ?x))
			(not (clear ?x))
			(not (handempty))
			(holding ?x)
		)
	)

    (:action pick-down
        :parameters (?x - block)
        :precondition (and (clear ?x) (handempty) (imply (clear ?x) (handempty)) )
        :effect (and
            (not (ontable ?x))
            (not (clear ?x))
            (not (handempty))
            (holding ?x)
        )
    )
)