from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "model.joblib"


def train():
    # 1. 加载 demo 数据
    iris = load_iris()
    X = iris.data
    y = iris.target

    # 2. 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # 3. 建议用 Pipeline，把标准化和模型绑定在一起
    # 这样推理时不会忘记做同样的预处理
    pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000)),
        ]
    )

    # 4. 训练模型
    pipeline.fit(X_train, y_train)

    # 5. 评估
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"Test accuracy: {acc:.4f}")

    # 6. 保存模型和元信息
    artifact = {
        "model": pipeline,
        "class_names": iris.target_names.tolist(),
        "feature_names": iris.feature_names,
        "n_features": X.shape[1],
    }

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, MODEL_PATH)

    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train()
