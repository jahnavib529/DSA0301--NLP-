def simulate_dfa(string):
    state = "q0"
    path = [state]

    transitions = {
        ("q0", "a"): "q1",
        ("q0", "b"): "q0",
        ("q1", "a"): "q1",
        ("q1", "b"): "q2",
        ("q2", "a"): "q1",
        ("q2", "b"): "q0"
    }

    for ch in string:
        if (state, ch) in transitions:
            state = transitions[(state, ch)]
            path.append(state)
        else:
            print("Invalid Input")
            return

    print("Transition Path:")
    print(" -> ".join(path))

    if state == "q2":
        print("Accepted")
    else:
        print("Rejected")

text = input("Enter String: ")
simulate_dfa(text)
