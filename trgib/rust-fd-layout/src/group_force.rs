use force::{Force, Point};
use many_body_force::ManyBodyForce;

#[derive(Copy, Clone, Debug)]
pub struct Group {
    pub x: f32,
    pub y: f32,
    pub dx: f32,
    pub dy: f32,
}

impl Group {
    pub fn new(x: f32, y: f32, dx: f32, dy: f32) -> Group {
        Group {
            x: x,
            y: y,
            dx: dx,
            dy: dy,
        }
    }
}

pub struct GroupForce {
    pub groups: Vec<Group>,
    pub node_groups: Vec<usize>,
    pub strength: f32,
}

impl GroupForce {
    pub fn new(groups: Vec<Group>, node_groups: Vec<usize>) -> GroupForce {
        GroupForce {
            groups,
            node_groups,
            strength: 0.1,
        }
    }
}

impl Force for GroupForce {
    fn apply(&self, points: &mut Vec<Point>, alpha: f32) {
        let groups = &self.groups;
        let node_groups = &self.node_groups;
        let mut vec: Vec<f32> = Vec::new();
        for group in groups {
            if group.dx > group.dy {
                vec.push(group.dy);
            }
            else {
                vec.push(group.dx);
            }
        }
        for i in 0..vec.len() {
            vec[i] = vec[i] / vec[vec.len()-1];
            vec[i] = 1. / vec[i];
        }
        // eprintln!("{:?}", vec);
        let k = self.strength * alpha;
        for (point, &g) in points.iter_mut().zip(node_groups) {
            point.vx += (groups[g].x - point.x) * k * vec[g];
            point.vy += (groups[g].y - point.y) * k * vec[g];
        }
        let many_body = ManyBodyForce::new();
        for g in 0..groups.len() {
            let group_point_indices = (0..points.len())
                .filter(|&i| node_groups[i] == g)
                .collect::<Vec<_>>();
            let mut group_points = group_point_indices
                .iter()
                .map(|&i| points[i])
                .collect::<Vec<_>>();
            many_body.apply(&mut group_points, alpha);
            for (&i, &point) in group_point_indices.iter().zip(group_points.iter()) {
                points[i] = point
            }
        }
    }
}
