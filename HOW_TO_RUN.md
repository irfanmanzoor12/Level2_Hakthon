# How to Run the Todo App

## ✅ FIXED: Import Issue Resolved

The module import issue has been fixed. You can now run the application!

---

## 🚀 Running the Application

### Method 1: Direct Run (Recommended)
```bash
cd /home/irfan/speckit_hackathon
python src/main.py
```

### Method 2: Run Tests
```bash
python test_app.py
```

### Method 3: Run Demo
```bash
python demo.py
```

---

## 🎮 Using the App

When you run `python src/main.py`, you'll see:

```
==================================================
  Welcome to Todo App - Phase I
  Spec-Driven Development with Claude Code
==================================================

=== TODO APP - MAIN MENU ===

1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

Enter your choice (1-6):
```

### Quick Start Guide

**1. Add a task:**
- Type `1` and press Enter
- Enter title: `Complete Phase I`
- Enter description: `Finish and submit`

**2. View tasks:**
- Type `2` and press Enter
- See all your tasks

**3. Mark complete:**
- Type `5` and press Enter
- Enter task ID: `1`
- Task is now marked complete!

**4. Update a task:**
- Type `3` and press Enter
- Enter task ID
- Choose what to update
- Enter new values

**5. Delete a task:**
- Type `4` and press Enter
- Enter task ID
- Type `yes` to confirm

**6. Exit:**
- Type `6` and press Enter

---

## ✅ Verification

All tests pass:
```bash
python test_app.py
# Output: ✓ ALL TESTS PASSED!
```

Demo works:
```bash
python demo.py
# Shows all 5 features working
```

---

## 📝 What Was Fixed

**Problem:**
```
ModuleNotFoundError: No module named 'src'
```

**Solution:**
- Updated imports in `src/main.py`
- Updated imports in `src/ui.py`
- Updated imports in `src/storage.py`
- Fixed imports in `test_app.py`
- Fixed imports in `demo.py`

All files now use relative imports that work from the project root.

---

## 🎯 Next Steps

Now that the app is working:

1. **Test it yourself:**
   ```bash
   python src/main.py
   ```

2. **Try all features**
   - Add tasks
   - View tasks
   - Update tasks
   - Mark complete
   - Delete tasks

3. **Prepare for submission:**
   - Create GitHub repo
   - Record demo video
   - Submit form

---

## 🆘 Troubleshooting

### Still having issues?

**Make sure you're in the right directory:**
```bash
pwd
# Should show: /home/irfan/speckit_hackathon
```

**Check if files exist:**
```bash
ls src/
# Should show: __init__.py main.py models.py storage.py ui.py
```

**Run from project root:**
```bash
cd ~/speckit_hackathon
python src/main.py
```

---

## ✨ Everything Works!

- ✅ App runs correctly
- ✅ All features working
- ✅ Tests passing
- ✅ Demo script working
- ✅ Ready for submission!

**Go ahead and try it now:**
```bash
python src/main.py
```

Enjoy! 🎉
