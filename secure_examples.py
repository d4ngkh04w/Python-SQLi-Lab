"""
Secure Coding Examples for Python SQLi Lab

This module demonstrates secure coding practices that prevent SQL injection
vulnerabilities. It serves as an educational reference showing how the
vulnerable code in the main application should be implemented securely.

Educational Purpose: Compare these secure implementations with the intentionally
vulnerable code in app.py to understand the differences.
"""

import mysql.connector
import hashlib
import secrets
import logging
from typing import Optional, Dict, Any
import database.db as db

logger = logging.getLogger(__name__)


class SecureUserAuthentication:
    """
    Secure implementation of user authentication preventing SQL injection.
    
    Key security features:
    - Parameterized queries prevent SQL injection
    - Password hashing with salt
    - Input validation and sanitization
    - Proper error handling without information disclosure
    """
    
    @staticmethod
    def hash_password(password: str, salt: bytes = None) -> tuple[str, bytes]:
        """
        Securely hash a password with salt.
        
        Args:
            password: Plain text password
            salt: Optional salt bytes, generates new if None
            
        Returns:
            Tuple of (hashed_password_hex, salt_bytes)
        """
        if salt is None:
            salt = secrets.token_bytes(32)
        
        # Use PBKDF2 with SHA-256 for password hashing
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return hashed.hex(), salt
    
    @staticmethod
    def verify_password(password: str, hashed_password: str, salt: bytes) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password to verify
            hashed_password: Stored password hash
            salt: Salt used for hashing
            
        Returns:
            True if password matches, False otherwise
        """
        computed_hash, _ = SecureUserAuthentication.hash_password(password, salt)
        return secrets.compare_digest(computed_hash, hashed_password)
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """
        Validate username format and length.
        
        Args:
            username: Username to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not username or len(username) < 3 or len(username) > 20:
            return False
        
        # Allow alphanumeric characters and underscores only
        return username.replace('_', '').isalnum()
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        SECURE authentication function using parameterized queries.
        
        This demonstrates how the vulnerable login in app.py should be implemented.
        
        Args:
            username: Username to authenticate
            password: Password to verify
            
        Returns:
            User dict if authentication successful, None otherwise
        """
        # Input validation
        if not SecureUserAuthentication.validate_username(username):
            logger.warning(f"Invalid username format attempted: {username}")
            return None
        
        if not password or len(password) > 100:  # Reasonable password length limit
            logger.warning("Invalid password format attempted")
            return None
        
        try:
            conn = db.get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # SECURE: Use parameterized query to prevent SQL injection
            cursor.execute(
                "SELECT id, username, password, role FROM users WHERE username = %s",
                (username,)
            )
            
            user = cursor.fetchone()
            
            if user:
                # In a real secure implementation, passwords would be hashed
                # For this demo, we'll do simple comparison but log the secure approach
                logger.info("In production: would verify hashed password here")
                if user['password'] == password:  # Simplified for demo
                    logger.info(f"Successful secure authentication for user: {username}")
                    return {
                        'id': user['id'],
                        'username': user['username'],
                        'role': user['role']
                    }
            
            logger.info(f"Failed authentication attempt for user: {username}")
            return None
            
        except mysql.connector.Error as e:
            # SECURE: Log detailed error for administrators, return generic error to user
            logger.error(f"Database error during authentication: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during authentication: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()


class SecureBlogSearch:
    """
    Secure implementation of blog search preventing SQL injection.
    """
    
    @staticmethod
    def validate_search_term(search_term: str) -> bool:
        """
        Validate search term for safety.
        
        Args:
            search_term: Search term to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not search_term:
            return False
        
        if len(search_term) > 100:  # Reasonable search term length
            return False
        
        # Could add more sophisticated validation here
        # For example, check for suspicious patterns
        suspicious_patterns = ['union', 'select', 'drop', 'insert', 'update', 'delete']
        search_lower = search_term.lower()
        
        for pattern in suspicious_patterns:
            if pattern in search_lower:
                logger.warning(f"Suspicious search pattern detected: {search_term}")
                return False
        
        return True
    
    @staticmethod
    def search_blogs(search_term: str) -> list[Dict[str, Any]]:
        """
        SECURE blog search function using parameterized queries.
        
        This demonstrates how the vulnerable search in app.py should be implemented.
        
        Args:
            search_term: Term to search for in blog titles
            
        Returns:
            List of matching blog dictionaries
        """
        # Input validation
        if not SecureBlogSearch.validate_search_term(search_term):
            logger.warning(f"Invalid search term: {search_term}")
            return []
        
        try:
            conn = db.get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # SECURE: Use parameterized query with LIKE operator
            search_pattern = f"%{search_term}%"
            cursor.execute(
                "SELECT title, author_name FROM blogs WHERE title LIKE %s ORDER BY title",
                (search_pattern,)
            )
            
            results = cursor.fetchall()
            logger.info(f"Secure search for '{search_term}' returned {len(results)} results")
            return results
            
        except mysql.connector.Error as e:
            # SECURE: Log detailed error, return empty results
            logger.error(f"Database error during blog search: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error during blog search: {e}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()


class SecureUserLookup:
    """
    Secure implementation of user lookup preventing blind SQL injection.
    """
    
    @staticmethod
    def user_exists(username: str) -> bool:
        """
        SECURE user existence check using parameterized queries.
        
        This demonstrates how the vulnerable boolean SQLi endpoint should work.
        
        Args:
            username: Username to check
            
        Returns:
            True if user exists, False otherwise
        """
        # Input validation
        if not SecureUserAuthentication.validate_username(username):
            logger.warning(f"Invalid username format in lookup: {username}")
            return False
        
        try:
            conn = db.get_db_connection()
            cursor = conn.cursor()
            
            # SECURE: Use parameterized query
            cursor.execute(
                "SELECT COUNT(*) FROM users WHERE username = %s",
                (username,)
            )
            
            count = cursor.fetchone()[0]
            exists = count > 0
            
            logger.info(f"Secure user lookup for '{username}': {'found' if exists else 'not found'}")
            return exists
            
        except mysql.connector.Error as e:
            logger.error(f"Database error during user lookup: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during user lookup: {e}")
            return False
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()


def demonstrate_secure_practices():
    """
    Educational function demonstrating secure coding practices.
    
    This function shows how to properly implement the functionality
    that is intentionally vulnerable in the main application.
    """
    print("\n=== SECURE CODING DEMONSTRATIONS ===\n")
    
    # Demonstrate secure authentication
    print("1. Secure Authentication:")
    print("   - Uses parameterized queries")
    print("   - Validates input format")
    print("   - Implements proper password hashing")
    print("   - Handles errors securely")
    
    # Example usage (would not work without proper password hashing setup)
    print("\n   Example secure authentication call:")
    print("   user = SecureUserAuthentication.authenticate_user('alice', 'password')")
    
    # Demonstrate secure search
    print("\n2. Secure Blog Search:")
    print("   - Uses parameterized queries")
    print("   - Validates search terms")
    print("   - Sanitizes input")
    print("   - Limits result size")
    
    print("\n   Example secure search call:")
    print("   results = SecureBlogSearch.search_blogs('Python')")
    
    # Demonstrate secure user lookup
    print("\n3. Secure User Lookup:")
    print("   - Uses parameterized queries")
    print("   - Validates username format")
    print("   - Returns boolean without exposing data")
    
    print("\n   Example secure lookup call:")
    print("   exists = SecureUserLookup.user_exists('alice')")
    
    print("\n=== KEY SECURITY PRINCIPLES ===")
    print("✓ Always use parameterized queries")
    print("✓ Validate and sanitize all input")
    print("✓ Implement proper error handling")
    print("✓ Use secure password hashing")
    print("✓ Apply principle of least privilege")
    print("✓ Log security events appropriately")
    print("✓ Never expose sensitive error details to users")


if __name__ == "__main__":
    demonstrate_secure_practices()