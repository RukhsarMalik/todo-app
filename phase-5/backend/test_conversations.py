"""
Test script for Conversation and Message models.

Validates:
- Conversation creation with valid user_id
- FK constraint rejects invalid user_id
- Message creation with role validation
- Message content validation
- Cascade delete behavior

Usage:
    uv run python test_conversations.py
    # or
    .venv/Scripts/python.exe test_conversations.py
"""

import asyncio
import logging
import sys
from uuid import uuid4

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def test_conversation_creation() -> bool:
    """
    T006/T007: Test creating a conversation for an existing user.

    Returns:
        bool: True if test passes, False otherwise.
    """
    from sqlmodel import select
    from db import _get_session_maker
    from models import User, Conversation

    logger.info("=" * 50)
    logger.info("TEST: Conversation Creation with Valid User")
    logger.info("=" * 50)

    try:
        session_maker = _get_session_maker()
        async with session_maker() as session:
            # First, get or create a test user
            result = await session.execute(select(User).limit(1))
            user = result.scalar_one_or_none()

            if not user:
                logger.warning("No users found. Creating test user...")
                from auth.password import hash_password
                user = User(
                    email=f"test-conv-{uuid4()}@example.com",
                    password_hash=hash_password("testpass123")
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)
                logger.info(f"Created test user: {user.id}")

            # Create a conversation
            conversation = Conversation(
                user_id=user.id,
                title="Test Conversation"
            )
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)

            # Verify it was created
            assert conversation.id is not None, "Conversation ID should not be None"
            assert conversation.user_id == user.id, "User ID should match"
            assert conversation.created_at is not None, "created_at should be set"
            assert conversation.updated_at is not None, "updated_at should be set"

            logger.info(f"✅ PASS: Conversation created: {conversation.id}")
            logger.info(f"   User ID: {conversation.user_id}")
            logger.info(f"   Title: {conversation.title}")
            logger.info(f"   Created at: {conversation.created_at}")

            return True

    except Exception as e:
        logger.error(f"❌ FAIL: {e}")
        return False


async def test_conversation_fk_constraint() -> bool:
    """
    T008: Test that FK constraint rejects invalid user_id.

    Returns:
        bool: True if test passes (constraint works), False otherwise.
    """
    from db import _get_session_maker
    from models import Conversation

    logger.info("=" * 50)
    logger.info("TEST: FK Constraint Rejects Invalid User ID")
    logger.info("=" * 50)

    try:
        session_maker = _get_session_maker()
        async with session_maker() as session:
            # Try to create conversation with non-existent user_id
            fake_user_id = str(uuid4())
            conversation = Conversation(
                user_id=fake_user_id,
                title="Should Fail"
            )
            session.add(conversation)
            await session.commit()

            # If we get here, the constraint didn't work
            logger.error("❌ FAIL: FK constraint did not reject invalid user_id")
            return False

    except Exception as e:
        error_msg = str(e).lower()
        if "foreign key" in error_msg or "violates" in error_msg or "constraint" in error_msg:
            logger.info("✅ PASS: FK constraint correctly rejected invalid user_id")
            logger.info(f"   Error: {type(e).__name__}")
            return True
        else:
            logger.error(f"❌ FAIL: Unexpected error: {e}")
            return False


async def test_message_creation_valid_role() -> bool:
    """
    T015: Test creating messages with valid roles.

    Returns:
        bool: True if test passes, False otherwise.
    """
    from sqlmodel import select
    from db import _get_session_maker
    from models import User, Conversation, Message

    logger.info("=" * 50)
    logger.info("TEST: Message Creation with Valid Role")
    logger.info("=" * 50)

    try:
        session_maker = _get_session_maker()
        async with session_maker() as session:
            # Get a user and create a conversation
            result = await session.execute(select(User).limit(1))
            user = result.scalar_one_or_none()

            if not user:
                logger.error("No users found. Run conversation tests first.")
                return False

            conversation = Conversation(user_id=user.id, title="Message Test")
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)

            # Test all valid roles
            for role in ["user", "assistant", "system"]:
                message = Message(
                    conversation_id=conversation.id,
                    role=role,
                    content=f"Test message with role: {role}"
                )
                session.add(message)
                await session.commit()
                await session.refresh(message)

                assert message.id is not None
                assert message.role == role
                logger.info(f"   Created message with role '{role}': {message.id}")

            logger.info("✅ PASS: All valid roles accepted")
            return True

    except Exception as e:
        logger.error(f"❌ FAIL: {e}")
        return False


async def test_message_role_validation() -> bool:
    """
    T016: Test that role validation rejects invalid roles.

    Returns:
        bool: True if test passes (validation works), False otherwise.
    """
    from models import Message

    logger.info("=" * 50)
    logger.info("TEST: Role Validation Rejects Invalid Roles")
    logger.info("=" * 50)

    try:
        # Try to create message with invalid role using model_validate
        message = Message.model_validate({
            "conversation_id": str(uuid4()),
            "role": "invalid_role",
            "content": "Test content"
        })
        logger.error("❌ FAIL: Role validation did not reject invalid role")
        return False

    except Exception as e:
        error_msg = str(e)
        if "role must be one of" in error_msg:
            logger.info("✅ PASS: Role validation correctly rejected invalid role")
            logger.info(f"   Error: role must be one of allowed values")
            return True
        else:
            logger.error(f"❌ FAIL: Unexpected error: {e}")
            return False


async def test_message_content_empty() -> bool:
    """
    T017: Test that content validation rejects empty content.

    Returns:
        bool: True if test passes (validation works), False otherwise.
    """
    from models import Message

    logger.info("=" * 50)
    logger.info("TEST: Content Validation Rejects Empty Content")
    logger.info("=" * 50)

    try:
        # Try to create message with empty content using model_validate
        message = Message.model_validate({
            "conversation_id": str(uuid4()),
            "role": "user",
            "content": ""
        })
        logger.error("❌ FAIL: Content validation did not reject empty content")
        return False

    except Exception as e:
        error_msg = str(e)
        if "content cannot be empty" in error_msg:
            logger.info("✅ PASS: Content validation correctly rejected empty content")
            logger.info(f"   Error: content cannot be empty")
            return True
        else:
            logger.error(f"❌ FAIL: Unexpected error: {e}")
            return False


async def test_message_content_too_long() -> bool:
    """
    T018: Test that content validation rejects content >10000 chars.

    Returns:
        bool: True if test passes (validation works), False otherwise.
    """
    from models import Message

    logger.info("=" * 50)
    logger.info("TEST: Content Validation Rejects >10000 Chars")
    logger.info("=" * 50)

    try:
        # Try to create message with too long content using model_validate
        long_content = "x" * 10001
        message = Message.model_validate({
            "conversation_id": str(uuid4()),
            "role": "user",
            "content": long_content
        })
        logger.error("❌ FAIL: Content validation did not reject long content")
        return False

    except Exception as e:
        error_msg = str(e)
        if "exceeds 10000 character limit" in error_msg:
            logger.info("✅ PASS: Content validation correctly rejected long content")
            logger.info(f"   Error: content exceeds 10000 character limit")
            return True
        else:
            logger.error(f"❌ FAIL: Unexpected error: {e}")
            return False


async def test_message_fk_constraint() -> bool:
    """
    T019: Test that FK constraint rejects invalid conversation_id.

    Returns:
        bool: True if test passes (constraint works), False otherwise.
    """
    from db import _get_session_maker
    from models import Message

    logger.info("=" * 50)
    logger.info("TEST: FK Constraint Rejects Invalid Conversation ID")
    logger.info("=" * 50)

    try:
        session_maker = _get_session_maker()
        async with session_maker() as session:
            # Try to create message with non-existent conversation_id
            fake_conversation_id = str(uuid4())
            message = Message(
                conversation_id=fake_conversation_id,
                role="user",
                content="Test content"
            )
            session.add(message)
            await session.commit()

            logger.error("❌ FAIL: FK constraint did not reject invalid conversation_id")
            return False

    except Exception as e:
        error_msg = str(e).lower()
        if "foreign key" in error_msg or "violates" in error_msg or "constraint" in error_msg:
            logger.info("✅ PASS: FK constraint correctly rejected invalid conversation_id")
            logger.info(f"   Error: {type(e).__name__}")
            return True
        else:
            logger.error(f"❌ FAIL: Unexpected error: {e}")
            return False


async def test_list_conversations_by_user() -> bool:
    """
    T020: Test listing conversations by user_id (most recent first).

    Returns:
        bool: True if test passes, False otherwise.
    """
    from sqlmodel import select
    from db import _get_session_maker
    from models import User, Conversation
    import time

    logger.info("=" * 50)
    logger.info("TEST: List Conversations by User ID")
    logger.info("=" * 50)

    try:
        session_maker = _get_session_maker()
        async with session_maker() as session:
            # Get a user
            result = await session.execute(select(User).limit(1))
            user = result.scalar_one_or_none()

            if not user:
                logger.error("No users found")
                return False

            # Create multiple conversations
            conv1 = Conversation(user_id=user.id, title="First Conversation")
            session.add(conv1)
            await session.commit()

            time.sleep(0.1)  # Small delay for different timestamps

            conv2 = Conversation(user_id=user.id, title="Second Conversation")
            session.add(conv2)
            await session.commit()

            # Query conversations for user (most recent first)
            result = await session.execute(
                select(Conversation)
                .where(Conversation.user_id == user.id)
                .order_by(Conversation.created_at.desc())
            )
            conversations = result.scalars().all()

            assert len(conversations) >= 2, "Should have at least 2 conversations"

            logger.info(f"✅ PASS: Found {len(conversations)} conversations for user")
            logger.info(f"   Most recent: {conversations[0].title}")
            return True

    except Exception as e:
        logger.error(f"❌ FAIL: {e}")
        return False


async def test_retrieve_messages_chronological() -> bool:
    """
    T021: Test retrieving messages by conversation_id (chronological order).

    Returns:
        bool: True if test passes, False otherwise.
    """
    from sqlmodel import select
    from db import _get_session_maker
    from models import User, Conversation, Message
    import time

    logger.info("=" * 50)
    logger.info("TEST: Retrieve Messages in Chronological Order")
    logger.info("=" * 50)

    try:
        session_maker = _get_session_maker()
        async with session_maker() as session:
            # Get a user and create conversation
            result = await session.execute(select(User).limit(1))
            user = result.scalar_one_or_none()

            if not user:
                logger.error("No users found")
                return False

            conversation = Conversation(user_id=user.id, title="Chronological Test")
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)

            # Create messages in order
            msg1 = Message(conversation_id=conversation.id, role="user", content="First message")
            session.add(msg1)
            await session.commit()

            time.sleep(0.1)

            msg2 = Message(conversation_id=conversation.id, role="assistant", content="Second message")
            session.add(msg2)
            await session.commit()

            time.sleep(0.1)

            msg3 = Message(conversation_id=conversation.id, role="user", content="Third message")
            session.add(msg3)
            await session.commit()

            # Query messages (chronological order - oldest first)
            result = await session.execute(
                select(Message)
                .where(Message.conversation_id == conversation.id)
                .order_by(Message.created_at.asc())
            )
            messages = result.scalars().all()

            assert len(messages) == 3, "Should have 3 messages"
            assert "First" in messages[0].content, "First message should be first"
            assert "Third" in messages[2].content, "Third message should be last"

            logger.info("✅ PASS: Messages retrieved in chronological order")
            for i, msg in enumerate(messages):
                logger.info(f"   {i+1}. [{msg.role}]: {msg.content[:30]}...")
            return True

    except Exception as e:
        logger.error(f"❌ FAIL: {e}")
        return False


async def test_empty_conversation_list() -> bool:
    """
    T022: Test empty list when user has no conversations.

    Returns:
        bool: True if test passes, False otherwise.
    """
    from sqlmodel import select
    from db import _get_session_maker
    from models import Conversation

    logger.info("=" * 50)
    logger.info("TEST: Empty List for Non-Existent User")
    logger.info("=" * 50)

    try:
        session_maker = _get_session_maker()
        async with session_maker() as session:
            # Query conversations for non-existent user
            fake_user_id = str(uuid4())
            result = await session.execute(
                select(Conversation).where(Conversation.user_id == fake_user_id)
            )
            conversations = result.scalars().all()

            assert len(conversations) == 0, "Should have no conversations"

            logger.info("✅ PASS: Empty list returned for user with no conversations")
            return True

    except Exception as e:
        logger.error(f"❌ FAIL: {e}")
        return False


async def test_cascade_delete_conversation() -> bool:
    """
    T023: Test cascade delete removes conversation and all its messages.

    Returns:
        bool: True if test passes, False otherwise.
    """
    from sqlmodel import select
    from db import _get_session_maker
    from models import User, Conversation, Message

    logger.info("=" * 50)
    logger.info("TEST: Cascade Delete Conversation and Messages")
    logger.info("=" * 50)

    try:
        session_maker = _get_session_maker()
        async with session_maker() as session:
            # Get a user
            result = await session.execute(select(User).limit(1))
            user = result.scalar_one_or_none()

            if not user:
                logger.error("No users found")
                return False

            # Create conversation with messages
            conversation = Conversation(user_id=user.id, title="To Be Deleted")
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)
            conv_id = conversation.id

            msg1 = Message(conversation_id=conv_id, role="user", content="Message 1")
            msg2 = Message(conversation_id=conv_id, role="assistant", content="Message 2")
            session.add(msg1)
            session.add(msg2)
            await session.commit()

            # Verify messages exist
            result = await session.execute(
                select(Message).where(Message.conversation_id == conv_id)
            )
            messages_before = result.scalars().all()
            assert len(messages_before) == 2, "Should have 2 messages before delete"

            # Delete conversation
            await session.delete(conversation)
            await session.commit()

            # Verify messages are also deleted (cascade)
            result = await session.execute(
                select(Message).where(Message.conversation_id == conv_id)
            )
            messages_after = result.scalars().all()
            assert len(messages_after) == 0, "Messages should be cascade deleted"

            logger.info("✅ PASS: Conversation and messages cascade deleted")
            logger.info(f"   Messages before: {len(messages_before)}")
            logger.info(f"   Messages after: {len(messages_after)}")
            return True

    except Exception as e:
        logger.error(f"❌ FAIL: {e}")
        return False


async def test_cascade_delete_user() -> bool:
    """
    T024: Test user cascade delete removes all their conversations and messages.

    Returns:
        bool: True if test passes, False otherwise.
    """
    from sqlmodel import select
    from db import _get_session_maker
    from models import User, Conversation, Message
    from auth.password import hash_password

    logger.info("=" * 50)
    logger.info("TEST: User Cascade Delete")
    logger.info("=" * 50)

    try:
        session_maker = _get_session_maker()
        async with session_maker() as session:
            # Create a new test user
            test_user = User(
                email=f"cascade-test-{uuid4()}@example.com",
                password_hash=hash_password("testpass")
            )
            session.add(test_user)
            await session.commit()
            await session.refresh(test_user)
            user_id = test_user.id

            # Create conversation with messages
            conversation = Conversation(user_id=user_id, title="User Cascade Test")
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)
            conv_id = conversation.id

            msg = Message(conversation_id=conv_id, role="user", content="Test message")
            session.add(msg)
            await session.commit()

            # Delete user
            await session.delete(test_user)
            await session.commit()

            # Verify conversation is deleted
            result = await session.execute(
                select(Conversation).where(Conversation.id == conv_id)
            )
            conv_after = result.scalar_one_or_none()
            assert conv_after is None, "Conversation should be cascade deleted"

            # Verify messages are deleted
            result = await session.execute(
                select(Message).where(Message.conversation_id == conv_id)
            )
            messages_after = result.scalars().all()
            assert len(messages_after) == 0, "Messages should be cascade deleted"

            logger.info("✅ PASS: User deletion cascaded to conversations and messages")
            return True

    except Exception as e:
        logger.error(f"❌ FAIL: {e}")
        return False


async def main() -> int:
    """
    Run all conversation and message tests.

    Returns:
        int: Exit code (0 if all pass, 1 if any fail).
    """
    from db import close_db

    results = []

    try:
        # Phase 3: Conversation tests
        # T006/T007: Test conversation creation
        results.append(await test_conversation_creation())

        # T008: Test FK constraint
        results.append(await test_conversation_fk_constraint())

        # Phase 4: Message tests
        # T015: Test message creation with valid roles
        results.append(await test_message_creation_valid_role())

        # T016: Test role validation
        results.append(await test_message_role_validation())

        # T017: Test empty content validation
        results.append(await test_message_content_empty())

        # T018: Test content length validation
        results.append(await test_message_content_too_long())

        # T019: Test message FK constraint
        results.append(await test_message_fk_constraint())

        # Phase 5: Retrieve history tests
        # T020: List conversations by user
        results.append(await test_list_conversations_by_user())

        # T021: Retrieve messages chronologically
        results.append(await test_retrieve_messages_chronological())

        # T022: Empty list for user with no conversations
        results.append(await test_empty_conversation_list())

        # Phase 6: Cascade delete tests
        # T023: Cascade delete conversation and messages
        results.append(await test_cascade_delete_conversation())

        # T024: User cascade delete
        results.append(await test_cascade_delete_user())

    finally:
        await close_db()

    # Summary
    logger.info("")
    logger.info("=" * 50)
    logger.info("TEST SUMMARY")
    logger.info("=" * 50)
    passed = sum(results)
    total = len(results)
    logger.info(f"Passed: {passed}/{total}")

    if all(results):
        logger.info("✅ All tests passed!")
        return 0
    else:
        logger.error("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
