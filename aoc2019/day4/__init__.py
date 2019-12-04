def valid_password(password: int, check_run: bool = False) -> bool:
    digits = [int(i) for i in str(password)]
    previous = digits[0]
    double = False
    run_len = 0
    for digit in digits[1:]:
        if digit < previous:
            return False
        if digit == previous:
            run_len += 1
        else:
            if run_len:
                if check_run:
                    if run_len == 1:
                        double = True
                else:
                    double = True

            run_len = 0
        previous = digit
    if run_len:
        if check_run:
            if run_len == 1:
                double = True
        else:
            double = True
    return double
