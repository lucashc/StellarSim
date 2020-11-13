#include <vector>
#include "geometry.hpp"

class OctNode {
private:
    float center, size;
    std::vector<Octnode*> children;
public:
    Octnode()


    void GenerateChildren(std::vector<vec3> points, std::vector<float> masses, std::vector<int> ids, std::vector<vec3> leaves){
        n = points.size();
        vector<vec3>[8] octant_points;  // contains a vector of points for each octant
        vector<float>[8] octant_masses; // contains a vector of masses for each octant
        vector<int>[8] octant_ids;      // i think you get the point
        vec3 center {this->center};
        for(int index = 0; index < n; ++index){  // assign each point (and corresponding mass) to an octant
            vec3 point = points[index]
            int i = point.x > center.x;
            int j = point.y > center.y;
            int k = point.z > center.z;
            int octant_index = 4*k + 2*j + i; // construct binary number to choose octant
            octant_points[octant_index].push_back(point);    // point = points[i]
            octant_masses[octant_index].push_back(masses[i]);
            octant_ids[octant_index].push_back(ids[i]);
        }

        for(int octant_index = 0; octant_index < 8, ++octant_index){  // create child nodes for each octant
            if(octant_points[octant_index].size() == 0){continue}
            float i = (octant_index>>2) % 2;  // not very elegant, but reverse-engineers i,j,k from octant index
            float j = (octant_index>>1) % 2;  // which we need to calculate the offset dx of the child node
            float k = octant_index % 2;
            dx = 0.5*this->size*(vec3(i-0.5,j-0.5,k-0.5));
            this->children.push_back(OctNode(center + dx, this->size/2, octant_masses[octant_index],
                                             octant_points[octant_index], octant_ids[octant_index], leaves));
        }
    }
}