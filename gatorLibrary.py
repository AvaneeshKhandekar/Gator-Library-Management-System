import sys

from red_black_tree import RedBlackTree


class GatorLibrary:

    # function to print book details to output file
    @staticmethod
    def write_book(nodes, file, book_id=None):
        for node in nodes:
            if node.book_id is not None:
                file.write(f"BookID = {node.book_id}\n")
                file.write(f"Title = {node.book_name}\n")
                file.write(f"Author = {node.author_name}\n")
                file.write(f"Availability = \"{node.availability_status}\"\n")
                file.write(f"BorrowedBy = {node.borrowed_by or 'None'}\n")
                file.write(f"Reservations = {list(node.reservation_heap.get_patrons_sorted())}\n\n")
            else:
                file.write(f"Book {book_id} not found in the library\n\n")

    # function to map operations from input file to functions
    @staticmethod
    def process_line(line, tree, output_file):
        if 'PrintBooks' in line:
            GatorLibrary.print_books(line, tree, output_file)
        elif 'PrintBook' in line:
            GatorLibrary.print_book(line, tree, output_file)
        elif 'InsertBook' in line:
            GatorLibrary.insert_book(line, tree)
        elif 'BorrowBook' in line:
            GatorLibrary.borrow_book(line, tree, output_file)
        elif 'ReturnBook' in line:
            GatorLibrary.return_book(line, tree, output_file)
        elif 'DeleteBook' in line:
            GatorLibrary.delete_book(line, tree, output_file)
        elif 'FindClosestBook' in line:
            GatorLibrary.find_closest_book(line, tree, output_file)
        elif 'ColorFlipCount' in line:
            GatorLibrary.get_color_flip_count(tree, output_file)
        elif 'Quit' in line:
            GatorLibrary.terminate(output_file)

    # function to retrieve books withing given range
    @staticmethod
    def print_books(line, tree, output_file):
        line = line[11:-1].split(',')
        books = tree.find_books_in_range(tree.root, int(line[0]), int(line[1]), [])
        GatorLibrary.write_book(books, output_file)

    # function to retrieve book with given id
    @staticmethod
    def print_book(line, tree, output_file):
        line = line[10:-1]
        book = tree.find_book(tree.root, int(line))
        GatorLibrary.write_book([book], output_file, line)

    # function to insert book into tree
    @staticmethod
    def insert_book(line, tree):
        line = line.replace('InsertBook', 'insert_book')
        exec(f'tree.{line}')

    # function to update book details and reservation queue when borrowed and print appropriate message
    @staticmethod
    def borrow_book(line, tree, output_file):
        line = line[11:-1].split(',')
        book, updated = tree.borrow_book(int(line[0]), int(line[1]), int(line[2]))
        if updated:
            output_file.write(f"Book {book.book_id} Borrowed by patron {line[0]}\n\n")
        else:
            output_file.write(f"Book {book.book_id} Reserved by patron {line[0]}\n\n")

    # function to update book details and reservation queue when returned and print appropriate message
    @staticmethod
    def return_book(line, tree, output_file):
        line = line[11:-1].split(',')
        book, returned = tree.return_book(int(line[1]))
        if returned:
            output_file.write(f"Book {book.book_id} Returned by patron {line[0]}\n\n")
            output_file.write(f"Book {book.book_id} Allotted to patron {returned}\n\n")
        else:
            output_file.write(f"Book {book.book_id} Returned by patron {line[0]}\n\n")

    # function to delete book with given id and notify waiting patrons
    @staticmethod
    def delete_book(line, tree, output_file):
        line = line[11:-1]
        book, waiting_list = tree.delete_book(int(line))
        if waiting_list:
            if len(waiting_list) == 1:
                output_file.write(
                    f"Book {book.book_id} is no longer available. Reservation made by Patron {waiting_list[0].patron_id} has been cancelled!\n\n")
            else:
                output_file.write(
                    f"Book {book.book_id} is no longer available. Reservations made by Patrons {', '.join(str(node.patron_id) for node in waiting_list)} have been cancelled!\n\n")
        else:
            output_file.write(f"Book {book.book_id} is no longer available\n\n")

    # function to find books closest to the given id
    @staticmethod
    def find_closest_book(line, tree, output_file):
        line = line[16:-1]
        books = tree.find_closest_book(int(line))
        GatorLibrary.write_book(books, output_file)

    # function to retrieve and print color flip count
    @staticmethod
    def get_color_flip_count(tree, output_file):
        output_file.write(f"Color Flip Count: {tree.get_color_flips()}\n\n")

    # function to terminate the program
    @staticmethod
    def terminate(output_file):
        output_file.write("Program Terminated!!")
        exit(0)

    # main function to read input file and open output file
    @staticmethod
    def main():
        input_file_name = sys.argv[1]
        output_file_name = f"{input_file_name[:-4]}_output_file.txt"

        with open(input_file_name, 'r') as input_file, open(output_file_name, 'w') as output_file:
            tree = RedBlackTree()

            for line in input_file.readlines():
                GatorLibrary.process_line(line.strip(), tree, output_file)

        output_file.close()
        input_file.close()


# entry point
if __name__ == "__main__":
    GatorLibrary.main()
