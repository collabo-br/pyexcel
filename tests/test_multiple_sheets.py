from base import PyexcelMultipleSheetBase
import pyexcel
import os
from base import create_sample_file1


class TestOdsNxlsMultipleSheets(PyexcelMultipleSheetBase):
    def setUp(self):
        self.testfile = "multiple1.ods"
        self.testfile2 = "multiple1.xls"
        self.content = {
            "Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
            "Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]],
            "Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        }
        self._write_test_file(self.testfile)

    def tearDown(self):
        self._clean_up()


class TestXlsNOdsMultipleSheets(PyexcelMultipleSheetBase):
    def setUp(self):
        self.testfile = "multiple1.xls"
        self.testfile2 = "multiple1.ods"
        self.content = {
            "Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
            "Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]],
            "Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        }
        self._write_test_file(self.testfile)

    def tearDown(self):
        self._clean_up()


class TestXlsNXlsmMultipleSheets(PyexcelMultipleSheetBase):
    def setUp(self):
        self.testfile = "multiple1.xls"
        self.testfile2 = "multiple1.xlsm"
        self.content = {
            "Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
            "Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]],
            "Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        }
        self._write_test_file(self.testfile)

    def tearDown(self):
        self._clean_up()

class TestSingleSheetReaderForMulitpleSheetBook:
    def setUp(self):
        self.testfile = "multiple1.xls"
        self.content = {
            "Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
            "Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]],
            "Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        }
        w = pyexcel.BookWriter(self.testfile)
        w.write_book_from_dict(self.content)
        w.close()

    def test_non_default_sheet_as_single_sheet_reader(self):
        r = pyexcel.Reader(self.testfile, "Sheet1")
        data = pyexcel.utils.to_array(r)
        assert data == self.content["Sheet1"]
        r2 = pyexcel.Reader(self.testfile, "Sheet2")
        data = pyexcel.utils.to_array(r2)
        assert data == self.content["Sheet2"]
        r3 = pyexcel.Reader(self.testfile, "Sheet3")
        data = pyexcel.utils.to_array(r3)
        assert data == self.content["Sheet3"]

    def test_non_default_sheet_as_single_sheet_reader_series(self):
        r = pyexcel.SeriesReader(self.testfile, "Sheet3")
        data = pyexcel.utils.to_array(r.rows())
        assert data == self.content["Sheet3"][1:]

    def test_non_default_sheet_as_single_sheet_plain_reader(self):
        r = pyexcel.PlainReader(self.testfile, "Sheet2")
        data = pyexcel.utils.to_array(r.rows())
        assert data == self.content["Sheet2"]

    def test_non_default_sheet_as_single_sheet_filterable_reader(self):
        r = pyexcel.FilterableReader(self.testfile, "Sheet2")
        data = pyexcel.utils.to_array(r.rows())
        assert data == self.content["Sheet2"]

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)


class TestReader:
    def setUp(self):
        """
        Make a test csv file as:

        a,b,c,d
        e,f,g,h
        i,j,1.1,1
        """
        self.testfile = "testcsv.csv"
        self.rows = 3
        create_sample_file1(self.testfile)

    def test_csv_book_reader(self):
        r = pyexcel.BookReader(self.testfile)
        assert r.number_of_sheets() == 1
        assert r.sheet_names() == ["csv"]

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)

class TestAddBooks:
    def _write_test_file(self, file):
        """
        Make a test file as:

        1,1,1,1
        2,2,2,2
        3,3,3,3
        """
        self.rows = 3
        w = pyexcel.BookWriter(file)
        w.write_book_from_dict(self.content)
        w.close()

    def setUp(self):
        self.testfile = "multiple1.ods"
        self.testfile2 = "multiple1.xls"
        self.testfile3 = "multiple2.xlsx"
        self.content = {
            "Sheet1": [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]],
            "Sheet2": [[4, 4, 4, 4], [5, 5, 5, 5], [6, 6, 6, 6]],
            "Sheet3": [[u'X', u'Y', u'Z'], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
        }
        self._write_test_file(self.testfile)
        self._write_test_file(self.testfile2)

    def test_delete_sheets(self):
        b1 = pyexcel.readers.Book(self.testfile)
        assert len(b1.sheet_names()) == 3
        del b1["Sheet1"]
        assert len(b1.sheet_names()) == 2
        try:
            del b1["Sheet1"]
            assert 1==2
        except KeyError:
            assert 1==1
        del b1[1]
        assert len(b1.sheet_names()) == 1
        try:
            del b1[1]
            assert 1==2
        except IndexError:
            assert 1==1
            
    def test_delete_sheets2(self):
        """repetitively delete first sheet"""
        b1 = pyexcel.readers.Book(self.testfile)
        del b1[0]
        assert len(b1.sheet_names()) == 2
        del b1[0]
        assert len(b1.sheet_names()) == 1
        del b1[0]
        assert len(b1.sheet_names()) == 0
        
    def test_add_book1(self):
        """
        test this scenario: book3 = book1 + book2
        """
        b1 = pyexcel.BookReader(self.testfile)
        b2 = pyexcel.BookReader(self.testfile2)
        b3 = b1 + b2
        content = pyexcel.utils.to_dict(b3)
        sheet_names = content.keys()
        assert len(sheet_names) == 6
        for name in sheet_names:
            if "Sheet3" in name:
                assert content[name] == self.content["Sheet3"]
            elif "Sheet2" in name:
                assert content[name] == self.content["Sheet2"]
            elif "Sheet1" in name:
                assert content[name] == self.content["Sheet1"]
        
    def test_add_book1_in_place(self):
        """
        test this scenario: book1 +=  book2
        """
        b1 = pyexcel.BookReader(self.testfile)
        b2 = pyexcel.BookReader(self.testfile2)
        b1 += b2
        content = pyexcel.utils.to_dict(b1)
        sheet_names = content.keys()
        assert len(sheet_names) == 6
        for name in sheet_names:
            if "Sheet3" in name:
                assert content[name] == self.content["Sheet3"]
            elif "Sheet2" in name:
                assert content[name] == self.content["Sheet2"]
            elif "Sheet1" in name:
                assert content[name] == self.content["Sheet1"]

    def test_add_book2(self):
        """
        test this scenario: book3 = book1 + sheet3
        """
        b1 = pyexcel.BookReader(self.testfile)
        b2 = pyexcel.BookReader(self.testfile2)
        b3 = b1 + b2["Sheet3"]
        content = pyexcel.utils.to_dict(b3)
        sheet_names = content.keys()
        assert len(sheet_names) == 4
        for name in sheet_names:
            if "Sheet3" in name:
                assert content[name] == self.content["Sheet3"]
            elif "Sheet2" in name:
                assert content[name] == self.content["Sheet2"]
            elif "Sheet1" in name:
                assert content[name] == self.content["Sheet1"]

    def test_add_book2_in_place(self):
        """
        test this scenario: book3 = book1 + sheet3
        """
        b1 = pyexcel.BookReader(self.testfile)
        b2 = pyexcel.BookReader(self.testfile2)
        b1 += b2["Sheet3"]
        content = pyexcel.utils.to_dict(b1)
        sheet_names = content.keys()
        assert len(sheet_names) == 4
        for name in sheet_names:
            if "Sheet3" in name:
                assert content[name] == self.content["Sheet3"]
            elif "Sheet2" in name:
                assert content[name] == self.content["Sheet2"]
            elif "Sheet1" in name:
                assert content[name] == self.content["Sheet1"]

    def test_add_book3(self):
        """
        test this scenario: book3 = sheet1 + sheet2
        """
        b1 = pyexcel.BookReader(self.testfile)
        b2 = pyexcel.BookReader(self.testfile2)
        b3 = b1["Sheet1"] + b2["Sheet3"]
        content = pyexcel.utils.to_dict(b3)
        sheet_names = content.keys()
        assert len(sheet_names) == 2
        assert content["Sheet3"] == self.content["Sheet3"]
        assert content["Sheet1"] == self.content["Sheet1"]
        
    def test_add_book4(self):
        """
        test this scenario: book3 = sheet1 + book
        """
        b1 = pyexcel.BookReader(self.testfile)
        b2 = pyexcel.BookReader(self.testfile2)
        b3 = b1["Sheet1"] + b2
        content = pyexcel.utils.to_dict(b3)
        sheet_names = content.keys()
        assert len(sheet_names) == 4
        for name in sheet_names:
            if "Sheet3" in name:
                assert content[name] == self.content["Sheet3"]
            elif "Sheet2" in name:
                assert content[name] == self.content["Sheet2"]
            elif "Sheet1" in name:
                assert content[name] == self.content["Sheet1"]

    def test_add_book_error(self):
        """
        test this scenario: book3 = sheet1 + book
        """
        b1 = pyexcel.BookReader(self.testfile)
        try:
            b1 + 12
            assert 1==2
        except TypeError:
            assert 1==1
        try:
            b1 += 12
            assert 1==2
        except TypeError:
            assert 1==1

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
        if os.path.exists(self.testfile2):
            os.unlink(self.testfile2)
