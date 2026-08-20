import cenos_py


def get_shaft_scanning_case(
    current: float, velocity: float, end_time: float
) -> cenos_py.CenosCaseIH:
    """Returns a Cenos case of Shaft scanning with the given current, velocity, and end time."""
    case = cenos_py.CenosCaseIH()
    case.set_pre_processor("geomFromCad", True)
    case.read_cad_files(["D:\\cases\\IH\\pythonAPI\\shaft_scanning.step"])
    case.set_geometry_type("workpieceHeating")
    case.add_air(True, ["Face_24", "Face_21", "Face_25", "Face_22"])
    case.assign_domain_role_py(["Solid_1"], "workpiece")
    case.assign_boundary_role_py(
        [
            "Face_2",
            "Face_3",
            "Face_4",
            "Face_5",
            "Face_7",
            "Face_8",
            "Face_9",
            "Face_10",
            "Face_11",
            "Face_12",
            "Face_13",
            "Face_14",
            "Face_15",
            "Face_16",
            "Face_17",
            "Face_18",
            "Face_19",
            "Face_20",
        ],
        "wp_surface3D",
    )
    case.add_role_entry("wp_axis3D")
    case.assign_boundary_role_py(["Face_1", "Face_6"], "wp_axis3D")
    case.update_tab_property("simulation", "tend", end_time)
    case.update_tab_property("simulation", "tstep", end_time / 50)
    case.assign_group_material("Solid_1", "steel1020_fullBH")
    case.update_material_property("Solid_1", "useBHModel", False)
    case.update_physics_property(
        "physicsElectromagnetics", "domain", "Solid_2", "frequency1", 25000
    )
    case.set_boundary_type("Face_21", "physicsElectromagnetics", "current")
    case.update_physics_property(
        "physicsElectromagnetics", "boundary", "Face_21", "I_3D", current
    )
    case.update_physics_property(
        "physicsElectromagnetics", "domain", "Solid_3", "frequency1", 25000
    )
    case.set_boundary_type("Face_25", "physicsElectromagnetics", "ground")
    case.update_physics_property(
        "physicsElectromagnetics", "boundary", "Face_24", "I_3D", current
    )
    case.entered_meshing_window()
    case.generate_mesh()
    case.set_motion_enabled("Motion", True)
    case.set_motion_domains("Motion", ["Solid_2"])
    case.set_motion_domains("Motion", ["Solid_2", "Solid_3"])
    case.update_motion_property("Motion", "Velocity_y", velocity)
    return case
