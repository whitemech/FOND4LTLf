(define (problem bw_0)
  (:domain blocks-domain)
  (:objects a b c d e - block)
  (:init
  		(emptyhand)
  		(ontable c) (on a c) (on b a) (clear b)
  		(ontable d) (on e d) (clear e))
  (:goal
  	(and
  		(emptyhand)
  		;(on a b) (clear a)
  		(on b e) (ontable e)
  		;(ontable c) (ontable d) (clear c) (clear d)
  	)
  )
)
