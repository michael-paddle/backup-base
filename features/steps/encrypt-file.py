import random
import string
from hamcrest import assert_that, not_, contains, equal_to, greater_than
import gpg
from tempfile import TemporaryDirectory
from typing import Any

given: Any
when: Any
then: Any


@given(u"that I have a file in my directory")
def step_impl(context):
    context.test_data = "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(16)]
    ).encode("utf-8")
    context.test_file_in = "testdata.dat"
    context.test_file_out = "testdata.dat.gpg"
    with open(context.test_file_in, "wb") as data_file:
        data_file.write(context.test_data)


@when(u"I run a script that calls my encryption command on that file")
def step_impl_1(context):  # type: ignore
    context.backup_context.run(["fixtures/encrypt_file.sh"])


@then(u"an encrypted file should be created")
def step_impl_2(context):
    with open(context.test_file_out, "rb") as data_file:
        context.encrypted_file_contents = data_file.read()
    assert_that(len(context.encrypted_file_contents), greater_than(10))
    assert_that(context.encrypted_file_contents, not_(contains(context.test_data)))


@then(
    u"if I decrypt that file the content with the private key it should match the original"
)
def step_impl_3(context):
    c = gpg.Context(armor=True)
    gpgdir = TemporaryDirectory()
    c.home_dir = gpgdir.name

    assert_that(
        len(context.private_key),
        greater_than(64),
        "private key is too short to be real",
    )
    assert_that(
        len(context.encrypted_file_contents),
        greater_than(64),
        "encrypted file is too short to be real ",
    )
    c.key_import(context.private_key)
    plaintext, result, verify_result = c.decrypt(context.encrypted_file_contents)
    assert_that(plaintext, equal_to(context.test_data))


@then(u"if I decrypt that file the content with the original GPG setup")
def step_impl_4(context):
    c = context.gpg_context
    plaintext, result, verify_result = c.decrypt(context.encrypted_file_contents)
    assert_that(plaintext, equal_to(context.test_data))


@then(u"I should be able to decrypt that file with each key provided")
def step_impl_5(context):
    for private_key in [x[2] for x in context.key_pair_list]:
        c = gpg.Context(armor=True)
        gpgdir = TemporaryDirectory()
        c.home_dir = gpgdir.name

        assert_that(
            len(private_key), greater_than(64), "private key is too short to be real"
        )
        assert_that(
            len(context.encrypted_file_contents),
            greater_than(64),
            "encrypted file is too short to be real ",
        )
        c.key_import(private_key)
        plaintext, result, verify_result = c.decrypt(context.encrypted_file_contents)
        assert_that(plaintext, equal_to(context.test_data))
