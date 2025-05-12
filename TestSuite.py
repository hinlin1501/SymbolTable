import unittest
from TestUtils import TestUtils


class TestSymbolTable(unittest.TestCase):
    def test_0(self):
        input = ["INSERT a1 number", "INSERT b2 string"]
        expected = ["success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 100))

    def test_1(self):
        input = ["INSERT x number", "INSERT y string", "INSERT x string"]
        expected = ["Redeclared: INSERT x string"]

        self.assertTrue(TestUtils.check(input, expected, 101))

    def test_2(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "ASSIGN x 15",
            "ASSIGN y 17",
            "ASSIGN x 'abc'",
        ]
        expected = ["TypeMismatch: ASSIGN y 17"]

        self.assertTrue(TestUtils.check(input, expected, 102))

    def test_3(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "END",
            "END",
        ]
        expected = ["success", "success", "success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 103))

    def test_4(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "LOOKUP x",
            "LOOKUP y",
            "END",
        ]
        expected = ["success", "success", "success", "1", "0"]

        self.assertTrue(TestUtils.check(input, expected, 104))

    def test_5(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "INSERT z number",
            "PRINT",
            "END",
        ]
        expected = ["success", "success", "success", "success", "y//0 x//1 z//1"]

        self.assertTrue(TestUtils.check(input, expected, 105))

    def test_6(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "INSERT z number",
            "RPRINT",
            "END",
        ]
        expected = ["success", "success", "success", "success", "z//1 x//1 y//0"]

        self.assertTrue(TestUtils.check(input, expected, 106))

    def test_7(self):
        input = [
            "INSERT  a number"
        ]
        expected = ["Invalid: INSERT  a number"]

        self.assertTrue(TestUtils.check(input, expected, 107))

    def test_8(self):
        input = [
            "INSERT a number "
        ]
        expected = ["Invalid: INSERT a number "]

        self.assertTrue(TestUtils.check(input, expected, 108))

    def test_9(self):
        input = [
            "BBEGIN",
            "BEGIN"
        ]
        expected = ["Invalid: BBEGIN"]

        self.assertTrue(TestUtils.check(input, expected, 109))

    def test_10(self):
        input = ["INSERT x number", "ASSIGN x 'abc'"]
        expected = ["TypeMismatch: ASSIGN x 'abc'"]

        self.assertTrue(TestUtils.check(input, expected, 110))

    def test_11(self):
        input = ["INSERT y string", "ASSIGN y 'hello'"]
        expected = ["success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 111))

    def test_12(self):
        input = ["INSERT x number", "INSERT y number", "ASSIGN y x"]
        expected = ["success", "success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 112))

    def test_13(self):
        input = ["ASSIGN x 5"]
        expected = ["Undeclared: ASSIGN x 5"]

        self.assertTrue(TestUtils.check(input, expected, 113))

    def test_14(self):
        input = ["INSERT x string", "ASSIGN x 10"]
        expected = ["TypeMismatch: ASSIGN x 10"]

        self.assertTrue(TestUtils.check(input, expected, 114))

    def test_15(self):
        input = ["INSERT x number", "ASSIGN x y"]
        expected = ["Undeclared: ASSIGN x y"]

        self.assertTrue(TestUtils.check(input, expected, 115))

    def test_16(self):
        input = ["INSERT Ba string"]
        expected = ["Invalid: INSERT Ba string"]

        self.assertTrue(TestUtils.check(input, expected, 116))

    def test_17(self):
        input = ["BEGIN", "INSERT x string", "INSERT y string", "END", "PRINT"]
        expected = ["success", "success", ""]

        self.assertTrue(TestUtils.check(input, expected, 117))

    def test_18(self):
        input = ["LOOKUP x"]
        expected = ["Undeclared: LOOKUP x"]

        self.assertTrue(TestUtils.check(input, expected, 118))

    def test_19(self):
        input = ["INSERT x string", "INSERT y string", "BEGIN", "BEGIN", "INSERT x string", "INSERT y string", "PRINT", "END", "INSERT x string", "INSERT y string", "END"]
        expected = ["success", "success", "success", "success", "x//2 y//2", "success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 119))

    def test_20(self):
        input = ["INSERT "]
        expected = ["Invalid: INSERT "]

        self.assertTrue(TestUtils.check(input, expected, 120))

    def test_21(self):
        input = ["INSERT * number"]
        expected = ["Invalid: INSERT * number"]

        self.assertTrue(TestUtils.check(input, expected, 121))

    def test_22(self):
        input = [" RPRINT"]
        expected = ["Invalid:  RPRINT"]

        self.assertTrue(TestUtils.check(input, expected, 122))

    def test_23(self):
        input = ["INSERT string bced"]
        expected = ["Invalid: INSERT string bced"]

        self.assertTrue(TestUtils.check(input, expected, 123))

    def test_24(self):
        input = ["INSERT 1bc string"]
        expected = ["Invalid: INSERT 1bc string"]

        self.assertTrue(TestUtils.check(input, expected, 124))

    def test_25(self):
        input = ["INSERT abc string number"]
        expected = ["Invalid: INSERT abc string number"]
        
        self.assertTrue(TestUtils.check(input, expected, 125))

    def test_26(self):
        input = ["RPRINT  "]
        expected = ["Invalid: RPRINT  "]

        self.assertTrue(TestUtils.check(input, expected, 126))

    def test_27(self):
        input = [""]
        expected = ["Invalid: "]

        self.assertTrue(TestUtils.check(input, expected, 127))

    def test_28(self):
        input = ["  "]
        expected = ["Invalid:   "]

        self.assertTrue(TestUtils.check(input, expected, 128))

    def test_29(self):
        input = ["INSERT x", "number INSERT y number"]
        expected = ["Invalid: INSERT x"]

        self.assertTrue(TestUtils.check(input, expected, 129))

    def test_30(self):
        input = ["INSERT x number", "  "]
        expected = ["Invalid:   "]

        self.assertTrue(TestUtils.check(input, expected, 130))

    def test_31(self):
        input = ["INSERT x string", "INSERT y string", "BEGIN", "INSERT z string", "RPRINT", "END"]
        expected = ["success", "success", "success", "z//1 y//0 x//0"]
        
        self.assertTrue(TestUtils.check(input, expected, 131))

    def test_32(self):
        input = [" BEGIN", "END"]
        expected = ["Invalid:  BEGIN"]

        self.assertTrue(TestUtils.check(input, expected, 132))

    def test_33(self):
        input = ["BEGIN ", "END"]
        expected = ["Invalid: BEGIN "]

        self.assertTrue(TestUtils.check(input, expected, 133))

    def test_34(self):
        input = ["INSERT x number", "BEGIN", "INSERT x number", "END"]
        expected = ["success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 134))

    def test_35(self):
        input = ["INSERT x number", "BEGIN", "INSERT x number", "ASSIGN x '1'", "END"]
        expected = ["TypeMismatch: ASSIGN x '1'"]

        self.assertTrue(TestUtils.check(input, expected, 135))

    def test_36(self):
        input = ["BEGIN", "BEGIN", "ASSIGN x y", "END", "END"]
        expected = ["Undeclared: ASSIGN x y"]

        self.assertTrue(TestUtils.check(input, expected, 136))

    def test_37(self):
        input = ["INSERT x number", "BEGIN", "INSERT x number", "BEGIN", "INSERT x number", "END", "ASSIGN x '1'"]
        expected = ["TypeMismatch: ASSIGN x '1'"]

        self.assertTrue(TestUtils.check(input, expected, 137))

    def test_38(self):
        input = ["BEGIN", "ASSIGN x 1", "INSERT x number", "INSERT y number", "END"]
        expected = ["Undeclared: ASSIGN x 1"]

        self.assertTrue(TestUtils.check(input, expected, 138))

    def test_39(self):
        input = ["INSERT x number", "END"]
        expected = ["UnknownBlock"]

        self.assertTrue(TestUtils.check(input, expected, 139))

    def test_40(self):
        input = ["BEGIN", "BEGIN", "BEGIN"]
        expected = ["UnclosedBlock: 3"]

        self.assertTrue(TestUtils.check(input, expected, 140))

    def test_41(self):
        input = ["BEGIN", "BEGIN", "BEGIN", "END", "END"]
        expected = ["UnclosedBlock: 1"]
        self.assertTrue(TestUtils.check(input, expected, 141))

    def test_42(self):
        input = ["INSERT x number", "BEGIN", "INSERT x number", "BEGIN", "INSERT x number", "BEGIN", ]
        expected = ["UnclosedBlock: 3"]

        self.assertTrue(TestUtils.check(input, expected, 142))

    def test_43(self):
        input = ["INSERT x number", "BEGIN", "LOOKUP x", "END"]
        expected = ["success", "0"]

        self.assertTrue(TestUtils.check(input, expected, 143))

    def test_44(self):
        input = ["LOOKUP "]
        expected = ["Invalid: LOOKUP "]

        self.assertTrue(TestUtils.check(input, expected, 144))

    def test_45(self):
        input = ["LOOKUP b_"]
        expected = ["Undeclared: LOOKUP b_"]

        self.assertTrue(TestUtils.check(input, expected, 145))

    def test_46(self):
        input = ["LOOKUP bc~ed"]
        expected = ["Invalid: LOOKUP bc~ed"]

        self.assertTrue(TestUtils.check(input, expected, 146))

    def test_47(self):
        input = ["INSERT x string", "INSERT y string", "BEGIN", "ASSIGN x 1", "INSERT x number", "INSERT y number", "END"]
        expected = ["TypeMismatch: ASSIGN x 1"]

        self.assertTrue(TestUtils.check(input, expected, 147))

    def test_48(self):
        input = ["INSERT x number", "BEGIN", "INSERT y string", "BEGIN", "INSERT z number", "ASSIGN x y", "END", "END"]
        expected = ["TypeMismatch: ASSIGN x y"]

        self.assertTrue(TestUtils.check(input, expected, 148))

    def test_49(self):
        input = ["LOOKUP b2"]
        expected = ["Undeclared: LOOKUP b2"]

        self.assertTrue(TestUtils.check(input, expected, 149))

    def test_50(self):
        input = [
        "INSERT a number",
        "ASSIGN a 123"
        ]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 150))

    def test_51(self):
        input = [
        "INSERT s string",
        "ASSIGN s 'bachkhoa'"
        ]
        expected = ["success", "success"]
        self.assertTrue(TestUtils.check(input, expected, 151))

    def test_52(self):
        input = [
            "END",
        ]
        expected = ["UnknownBlock"]
        self.assertTrue(TestUtils.check(input, expected, 152))







    

