(define (problem tire_19_0_28845)
  (:domain sptire)
  (:objects n0 - location
            na1 na2 na3 na4 na5 na6 na7 na8 na9 - location
            nb1 nb2 nb3 nb4 nb5 nb6 nb7 nb8 nb9 nb10 nb11 nb12 nb13 nb14 nb15 nb16 nb17 - location
            ng - location
            t1 t2 t3 t4 t5 t6 t7 t8 t9 t10 - tire)
  (:init (vehicle-at n0)

         (road n0 na1) (road na1 n0)
         (road na1 na2) (road na2 na1)
         (road na2 na3) (road na3 na2)
         (road na3 na4) (road na4 na3)
         (road na4 na5) (road na5 na4)
         (spiky-road na5 na6) (spiky-road na6 na5)
         (spiky-road na6 na7) (spiky-road na7 na6)         
         (road na7 ng) (road ng na7)

         (road n0 nb1) (road nb1 n0)
         (road nb1 nb2) (road nb2 nb1)
         (road nb2 nb3) (road nb3 nb2)
         (road nb3 nb4) (road nb4 nb3)
         (road nb4 nb5) (road nb5 nb4)
         (road nb5 nb6) (road nb6 nb5)
         (road nb6 nb7) (road nb7 nb6)
         (road nb7 nb8) (road nb8 nb7)
         (road nb8 nb9) (road nb9 nb8)
         (road nb9 nb10) (road nb10 nb9)
         (road nb10 nb11) (road nb11 nb10)
         ;(road nb11 ng) (road ng nb11)
         (road nb11 nb12) (road nb12 nb11)
         (road nb12 nb13) (road nb13 nb12)
         (road nb13 nb14) (road nb14 nb13)
         (spiky-road nb14 nb15) (spiky-road nb15 nb14)
         (road nb15 nb16) (road nb16 nb15)
         (road nb16 nb17) (road nb17 nb16)
         (road nb17 ng) (road ng nb17)

         (tire-at t1 na1)
         (tire-at t2 na1)
         (tire-at t3 na1)
         (tire-at t4 na1)
         (tire-at t5 na1)
         (tire-at t6 na1)
         (tire-at t7 na1)
         (tire-at t8 na1)
         (tire-at t9 na1)
         (tire-at t10 na1)

         (not-flattire)
         (not-hasspare)
  )
  (:goal (vehicle-at ng))
)