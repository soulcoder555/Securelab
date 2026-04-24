#!/usr/bin/env python3
"""
Claims Validation Script for SecureLab

This script demonstrates how to check all user claims/permissions
in the SecureLab Flask application.

Usage:
    python check_claims.py

Or from within the Flask shell:
    from app.utils.security import check_all_users_claims
    result = check_all_users_claims()
    print(result)
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.utils.security import check_all_users_claims

def main():
    """Check all user claims and display results."""
    app = create_app()

    with app.app_context():
        # Ensure database tables exist
        from app.extensions import db
        db.create_all()

        print("🔍 Checking all user claims in SecureLab...")
        print("=" * 50)

        result = check_all_users_claims()

        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return 1

        print(f"📊 Total Users: {result['total_users']}")
        print(f"✅ Valid Claims: {result['valid_users']}")
        print(f"❌ Invalid Claims: {len(result['invalid_users'])}")
        print(f"🎯 All Valid: {'Yes' if result['all_valid'] else 'No'}")
        print()

        if result['invalid_users']:
            print("🚨 Issues Found:")
            for invalid_user in result['invalid_users']:
                print(f"  • User '{invalid_user['username']}' (ID: {invalid_user['user_id']}): {invalid_user['issue']}")
        else:
            print("🎉 All user claims are valid!")

        print()
        print("💡 Tip: Access this check via the admin dashboard at /admin/check-claims")
        print("   or get JSON response at /admin/check-claims?json=1")

        return 0 if result['all_valid'] else 1

if __name__ == "__main__":
    sys.exit(main())