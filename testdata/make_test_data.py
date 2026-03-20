import csv,json,os,random

def make_test_csv():
    # Define the path for the CSV file
    csv_file_path = os.path.join(os.path.dirname(__file__), 'test_data.csv')

    # Sample data to write to the CSV file
    length = 1000
    dt     = 0.1
    data   = [['time','a','b','c']]
    for i in range(length):
        time = i * dt
        a = i * -2.0
        b = i *  3.0 + (i *  3.0 )*random.uniform(-0.1, 0.1)  # Adding some noise to 'b'
        c = i *  4.0 + random.uniform(-0.5, 0.5)  # Adding some noise to 'b'
        data.append([time, a, b, c])

    # Write data to the CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(f"Test CSV file created at: {csv_file_path}")


def make_test_3d_scene():
    import math
    scene = {}
    scene['objects'] = []
    scene['objects'].append({
        'name': 'Cube1',
        'type': 'cube',
        'position': [0, 0, 0],
        'size': [1, 1, 1],
        'color': [1, 0, 0],
        'rotation': [[1, 0, 0],[0, 1, 0],[0, 0, 1]],
        'scale': [1, 1, 1],
        'visible': True,
        'shape': 'cube',
    })
    scene['objects'].append({
        'name': 'Sphere1',
        'type': 'sphere',
        'position': [-2, 0, 0],
        'size': [1, 1, 1],
        'color': [0, 0, 1, 1],
        'rotation': [[1, 0, 0],[0, 1, 0],[0, 0, 1]],
        'scale': [1, 1, 1],
        'visible': True,
        'shape': 'sphere',
        'transforms':{
            'time': [i*0.1 for i in range(200)],
            'position': [
                [ [math.sin(i*0.1), math.cos(i*0.1), 0] for i in range(200)]
            ],
        }
    })
    scene['name'] = 'Test Scene'
    

    # Save the scene to a file
    import json 
    scene_file_path = os.path.join(os.path.dirname(__file__), 'test_scene.json3d')
    with open(scene_file_path, 'w') as f:
        json.dump(scene, f, indent=4)
    print(f"Test 3D scene created at: {scene_file_path}")

if __name__ == "__main__":
    make_test_csv()
    make_test_3d_scene()
    print("Test data generation complete.")