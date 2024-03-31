from task1.elections import Election
from task1.file_service import FileService


def input_function_for_task1():
    election = Election()

    file_service = FileService(election.candidates_dict)

    file_service.serialize_using_pickle()
    file_service.serialize_using_csv()

    deserialized_data_pickle = file_service.deserialize_using_pickle()
    deserialized_data_csv = file_service.deserialize_using_csv()
    print("Deserialized data using pickle: ", deserialized_data_pickle)
    print("Deserialized data using csv: ", deserialized_data_csv)

    election.initialize_candidates_using_dict(deserialized_data_pickle)

    print("\nList of candidates created using deserialized data: ")

    for i in election.candidates:
        print(i.name, i.votes)

    print("\nWinner/s of election:")
    for i in election.get_winners():
        print(i.name, i.votes)

    while True:
        name_of_candidate = input("Input name of a candidate: ")
        candidate = election.get_candidate_info(name_of_candidate)
        if candidate is None:
            break

        print(candidate.votes)


