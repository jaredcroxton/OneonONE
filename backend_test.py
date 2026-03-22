#!/usr/bin/env python3
"""
PerformOS One-on-One Builder V2 - Backend API Testing
Tests all V2 API endpoints with manager and team member credentials
"""

import requests
import sys
import json
from datetime import datetime

class PerformOSAPITester:
    def __init__(self, base_url="https://exact-port.preview.emergentagent.com"):
        self.base_url = base_url
        self.manager_token = None
        self.team_member_token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")
            self.failed_tests.append(f"{name}: {details}")

    def make_request(self, method, endpoint, token=None, data=None, expected_status=200):
        """Make API request with error handling"""
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = f'Bearer {token}'

        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == 'PATCH':
                response = requests.patch(url, json=data, headers=headers, timeout=10)
            else:
                return False, f"Unsupported method: {method}"

            success = response.status_code == expected_status
            if success:
                try:
                    return True, response.json()
                except:
                    return True, response.text
            else:
                return False, f"Status {response.status_code}: {response.text[:200]}"

        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {str(e)}"

    def test_root_endpoint(self):
        """Test backend API root endpoint"""
        # Test with a proper email format to check API connectivity
        success, data = self.make_request('POST', 'api/auth/login', 
                                        data={"email": "test@test.com", "password": "test"}, 
                                        expected_status=401)
        if success or ("Incorrect email or password" in str(data)):
            self.log_test("Backend API connectivity", True)
            return True
        else:
            self.log_test("Backend API connectivity", False, str(data))
            return False

    def test_manager_login(self):
        """Test manager login"""
        login_data = {
            "email": "alex@performos.io",
            "password": "demo"
        }
        success, data = self.make_request('POST', 'api/auth/login', data=login_data)
        
        if success and isinstance(data, dict) and 'access_token' in data:
            self.manager_token = data['access_token']
            user = data.get('user', {})
            if user.get('role') == 'manager' and user.get('name') == 'Alex Chen':
                self.log_test("Manager login", True)
                return True
            else:
                self.log_test("Manager login", False, f"Invalid user data: {user}")
                return False
        else:
            self.log_test("Manager login", False, str(data))
            return False

    def test_team_member_login(self):
        """Test team member login"""
        login_data = {
            "email": "sarah@performos.io",
            "password": "demo"
        }
        success, data = self.make_request('POST', 'api/auth/login', data=login_data)
        
        if success and isinstance(data, dict) and 'access_token' in data:
            self.team_member_token = data['access_token']
            user = data.get('user', {})
            if user.get('role') == 'team_member' and user.get('name') == 'Sarah Mitchell':
                self.log_test("Team member login", True)
                return True
            else:
                self.log_test("Team member login", False, f"Invalid user data: {user}")
                return False
        else:
            self.log_test("Team member login", False, str(data))
            return False

    def test_manager_auth_me(self):
        """Test manager /auth/me endpoint"""
        success, data = self.make_request('GET', 'api/auth/me', token=self.manager_token)
        
        if success and isinstance(data, dict) and data.get('role') == 'manager':
            self.log_test("Manager auth/me", True)
            return True
        else:
            self.log_test("Manager auth/me", False, str(data))
            return False

    def test_manager_members(self):
        """Test manager members endpoint"""
        success, data = self.make_request('GET', 'api/members', token=self.manager_token)
        
        if success and isinstance(data, list) and len(data) == 6:
            # Check if we have the expected team members
            member_names = [m.get('name') for m in data]
            expected_names = ['Sarah Mitchell', 'James Rodriguez', 'Priya Sharma', 'Marcus Thompson', 'Emily Nakamura', 'David O\'Brien']
            if all(name in member_names for name in expected_names):
                self.log_test("Manager members list", True)
                return True, data
            else:
                self.log_test("Manager members list", False, f"Missing expected members. Got: {member_names}")
                return False, data
        else:
            self.log_test("Manager members list", False, f"Expected 6 members, got: {len(data) if isinstance(data, list) else 'non-list'}")
            return False, data

    def test_manager_sessions(self):
        """Test manager sessions endpoint"""
        success, data = self.make_request('GET', 'api/sessions', token=self.manager_token)
        
        if success and isinstance(data, list) and len(data) >= 7:
            # Check if we have sessions with proper structure
            session_count = len(data)
            completed_sessions = [s for s in data if s.get('status') == 'completed']
            self.log_test("Manager sessions list", True, f"Found {session_count} sessions, {len(completed_sessions)} completed")
            return True, data
        else:
            self.log_test("Manager sessions list", False, f"Expected >=7 sessions, got: {len(data) if isinstance(data, list) else 'non-list'}")
            return False, data

    def test_manager_flags(self):
        """Test manager flags endpoint"""
        success, data = self.make_request('GET', 'api/flags?status=open', token=self.manager_token)
        
        if success and isinstance(data, list) and len(data) >= 6:
            # Check flag structure
            flag_categories = [f.get('category') for f in data]
            expected_categories = ['wellbeing', 'workload', 'psychological_safety', 'team_dynamics', 'manager_gap']
            found_categories = set(flag_categories)
            if any(cat in found_categories for cat in expected_categories):
                self.log_test("Manager flags list", True, f"Found {len(data)} flags with categories: {list(found_categories)}")
                return True, data
            else:
                self.log_test("Manager flags list", False, f"No expected flag categories found. Got: {list(found_categories)}")
                return False, data
        else:
            self.log_test("Manager flags list", False, f"Expected >=6 flags, got: {len(data) if isinstance(data, list) else 'non-list'}")
            return False, data

    def test_manager_dashboard_stats(self):
        """Test manager dashboard stats endpoint"""
        success, data = self.make_request('GET', 'api/stats/dashboard', token=self.manager_token)
        
        if success and isinstance(data, dict):
            required_keys = ['upcoming_sessions', 'completed_this_month', 'team_health_score', 'active_flags']
            if all(key in data for key in required_keys):
                stats = {k: data[k] for k in required_keys}
                self.log_test("Manager dashboard stats", True, f"Stats: {stats}")
                return True, data
            else:
                missing_keys = [k for k in required_keys if k not in data]
                self.log_test("Manager dashboard stats", False, f"Missing keys: {missing_keys}")
                return False, data
        else:
            self.log_test("Manager dashboard stats", False, str(data))
            return False, data

    def test_team_member_members(self):
        """Test team member members endpoint (should return only their own record)"""
        success, data = self.make_request('GET', 'api/members', token=self.team_member_token)
        
        if success and isinstance(data, list) and len(data) == 1:
            member = data[0]
            if member.get('name') == 'Sarah Mitchell' and member.get('email') == 'sarah@performos.io':
                self.log_test("Team member members list", True)
                return True, data
            else:
                self.log_test("Team member members list", False, f"Wrong member data: {member}")
                return False, data
        else:
            self.log_test("Team member members list", False, f"Expected 1 member, got: {len(data) if isinstance(data, list) else 'non-list'}")
            return False, data

    def test_team_member_sessions(self):
        """Test team member sessions endpoint"""
        success, data = self.make_request('GET', 'api/sessions', token=self.team_member_token)
        
        if success and isinstance(data, list):
            # Sarah should have at least 1 session based on seed data
            if len(data) >= 1:
                session = data[0]
                if 'date' in session and 'status' in session:
                    self.log_test("Team member sessions list", True, f"Found {len(data)} sessions")
                    return True, data
                else:
                    self.log_test("Team member sessions list", False, f"Invalid session structure: {session}")
                    return False, data
            else:
                self.log_test("Team member sessions list", False, "No sessions found for Sarah")
                return False, data
        else:
            self.log_test("Team member sessions list", False, str(data))
            return False, data

    def test_unauthorized_access(self):
        """Test that endpoints require proper authorization"""
        # Test without token
        success, data = self.make_request('GET', 'api/members', expected_status=401)
        if not success and "401" in str(data):
            self.log_test("Unauthorized access protection", True)
            return True
        else:
            self.log_test("Unauthorized access protection", False, "Should require authentication")
            return False

    def run_all_tests(self):
        """Run all backend tests"""
        print("🧪 Starting PerformOS Backend API Tests")
        print(f"🌐 Testing against: {self.base_url}")
        print("=" * 60)

        # Basic connectivity
        if not self.test_root_endpoint():
            print("❌ Backend API connectivity failed - stopping tests")
            return False

        # Authentication tests
        if not self.test_manager_login():
            print("❌ Manager login failed - stopping tests")
            return False

        if not self.test_team_member_login():
            print("❌ Team member login failed - stopping tests")
            return False

        # Manager endpoint tests
        self.test_manager_auth_me()
        members_success, members_data = self.test_manager_members()
        sessions_success, sessions_data = self.test_manager_sessions()
        flags_success, flags_data = self.test_manager_flags()
        stats_success, stats_data = self.test_manager_dashboard_stats()

        # Team member endpoint tests
        self.test_team_member_members()
        self.test_team_member_sessions()

        # Security tests
        self.test_unauthorized_access()

        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        
        if self.failed_tests:
            print("\n❌ Failed Tests:")
            for failure in self.failed_tests:
                print(f"   • {failure}")
        
        # Verify seed data
        print("\n📋 Seed Data Verification:")
        if members_success and isinstance(members_data, list):
            print(f"   ✅ Team Members: {len(members_data)}/6 loaded")
        if sessions_success and isinstance(sessions_data, list):
            print(f"   ✅ Sessions: {len(sessions_data)} loaded")
        if flags_success and isinstance(flags_data, list):
            print(f"   ✅ Flags: {len(flags_data)} loaded")

        success_rate = (self.tests_passed / self.tests_run) * 100
        print(f"\n🎯 Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 80

def main():
    """Main test runner"""
    tester = PerformOSAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())