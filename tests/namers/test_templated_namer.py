'''

TEST_CASE("Test StringTemplates")
{
    // begin-snippet: templated_custom_namer_example
    ApprovalTests::TemplatedCustomNamer namer(
        "/my/source/directory/{ApprovedOrReceived}/"
        "{TestFileName}.{TestCaseName}.{FileExtension}");
    // end-snippet

    CHECK(namer.getApprovedFileAsPath(".txt").toString("/") ==
          "/my/source/directory/approved/"
          "TemplatedCustomNamerExamples.Test_StringTemplates.txt");
    CHECK(namer.getReceivedFileAsPath(".txt").toString("/") ==
          "/my/source/directory/received/"
          "TemplatedCustomNamerExamples.Test_StringTemplates.txt");
}
'''
from typing import Optional

from approvaltests import get_default_namer, verify, Namer, StackFrameNamer


class TemplatedCustomNamer(Namer):
    def __init__(self, template: str):
        self.template = template

        self.stacktracenamer = StackFrameNamer()

    def get_received_filename(self, base: Optional[str] = None) -> str:
        return self.template.format(
            approved_or_received="received",
            test_file_name=self.stacktracenamer.get_class_name(),
            test_case_name="test_get_received_filename",
            file_extension='txt')

    def get_approved_filename(self, base: Optional[str] = None) -> str:
        return self.template.format(
            approved_or_received="approved",
            test_file_name=self.stacktracenamer.get_class_name(),
            test_case_name="test_get_approved_filename",
            file_extension='txt')


def test_get_received_filename():
    namer = TemplatedCustomNamer(
        "/my/source/directory/{approved_or_received}/{test_file_name}.{test_case_name}.{file_extension}"
    )
    assert (namer.get_received_filename() == "/my/source/directory/received/"
                                             "test_templated_namer.test_get_received_filename.txt")


def test_get_approved_filename():
    namer = TemplatedCustomNamer(
        "/my/source/directory/{approved_or_received}/{test_file_name}.{test_case_name}.{file_extension}"
    )
    assert (namer.get_approved_filename() == "/my/source/directory/approved/"
                                             "test_templated_namer.test_get_approved_filename.txt")
