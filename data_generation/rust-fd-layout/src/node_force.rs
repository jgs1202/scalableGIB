use std::collections::HashMap;
use force::{Point, Link, Force};

pub struct PointForce {
    points: Vec<Points>,
    pub strength_nodes: f32,
    pub nodes_in_group: Vec<usize>
}

impl PointForce {
    pub fn new(points: &Vec<Points>, nodes_in_group: Vec<usize>) -> PointForce {
        PointForce {
            points: points.clone().to_vec(),
            nodes_in_group,
            strength_nodes: 0.1,
         }
    }
}

impl Force for PointForce {
    fn apply(&self, alpha: f32) {
        let nodes_in_group = &self.nodes_in_group
        let points = &self.points;
        // let node_groups = &self.node_groups;
        let k = self.strength * alpha;
        for i in nodes_in_group{
            if i.len() != 0 {
                for j in 0..(i.len() - 1 ) {
                    for k in 0..(i.len() - j - 1){
                        points[ i[j] ].vx += ( points[ i[j] ].x - points[ i[j+k+1] ].x ) * k;
                        points[ i[j+k+1] ].vx += ( points[ i[j+k+1] ].x - points[ i[j] ].x ) * k;
                        points[ i[j] ].vy += ( points[ i[j] ].y - points[ i[j+y+1] ].y ) * k;
                        points[ i[j+k+1] ].vy += ( points[ i[j+k+1] ].y - points[ i[j] ].y ) * k;
                        // eprintln!("{}, {}", i[j], i[j+k+1]);
                    }
                }
            }
        }

        for (point, &g) in points.iter_mut().zip(node_groups) {
            point.vx += (groups[g].x - point.x) * k;
            point.vy += (groups[g].y - point.y) * k;
        }



    }
}
