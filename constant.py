DEFAULT_LUCK_LIST = ["大吉","中吉","小吉","末吉","吉带凶","中平","凶带吉","小凶","凶","大凶"]
NUM_EVENTS = 6
SUPPORT_MODELS = ["deepseek-chat","deepseek-reasoner"]
DATA_DIR = "./data"
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ name }}的今日运势 - {{ date }}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Comic Sans MS', 'Marker Felt', '楷体', sans-serif;
        }

        body {
            background: linear-gradient(135deg, #ffd6e7, #c1e3ff);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            width: 100%;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            position: relative;
        }

        .header {
            background: linear-gradient(90deg, #ff85a2, #ffc2d1);
            padding: 30px 20px;
            text-align: center;
            position: relative;
            color: white;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }

        .header .date {
            font-size: 1.2rem;
            opacity: 0.9;
        }

        .fortune-result {
            padding: 30px;
            text-align: center;
            font-size: 1.8rem;
            color: #ff6b6b;
            font-weight: bold;
            background: rgba(255, 245, 245, 0.7);
            margin: 20px;
            border-radius: 15px;
            position: relative;
        }

        .fortune-icon {
            font-size: 3rem;
            margin-bottom: 15px;
            display: inline-block;
            animation: bounce 2s infinite;
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }

        .tips {
            background: #fff9c4;
            padding: 20px;
            margin: 0 20px 20px;
            border-radius: 15px;
            font-size: 1.3rem;
            position: relative;
            border-left: 5px solid #ffd54f;
        }

        .tips:before {
            content: "💡";
            position: absolute;
            left: 10px;
            top: -15px;
            font-size: 2rem;
        }

        .sections {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            padding: 0 20px 30px;
        }

        .section {
            flex: 1;
            min-width: 300px;
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            position: relative;
            overflow: hidden;
        }

        .section:before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 8px;
        }

        .good-section:before {
            background: linear-gradient(90deg, #a8e6cf, #6dd5ed);
        }

        .bad-section:before {
            background: linear-gradient(90deg, #ffafbd, #ffc3a0);
        }

        .section h2 {
            font-size: 1.8rem;
            margin-bottom: 20px;
            color: #444;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .good-section h2 {
            color: #4caf50;
        }

        .bad-section h2 {
            color: #f44336;
        }

        .activity {
            background: #f9f9f9;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            transition: transform 0.3s;
        }

        .activity:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        .activity-icon {
            width: 50px;
            height: 50px;
            background: #ffe0e0;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-right: 15px;
            font-size: 1.5rem;
            flex-shrink: 0;
        }

        .good-section .activity-icon {
            background: #e0f7fa;
            color: #26c6da;
        }

        .bad-section .activity-icon {
            background: #ffebee;
            color: #ef5350;
        }

        .activity-content {
            text-align: left;
        }

        .activity-title {
            font-weight: bold;
            font-size: 1.3rem;
            margin-bottom: 5px;
        }

        .activity-desc {
            color: #666;
            font-size: 1.1rem;
        }

        .footer {
            text-align: center;
            padding: 20px;
            color: #888;
            font-size: 0.9rem;
            background: #f8f9fa;
        }

        .decoration {
            position: absolute;
            z-index: -1;
            opacity: 0.2;
        }

        .decoration-1 {
            top: 10%;
            left: 5%;
            font-size: 5rem;
            transform: rotate(-20deg);
        }

        .decoration-2 {
            bottom: 10%;
            right: 5%;
            font-size: 6rem;
            transform: rotate(15deg);
        }

        .character {
            position: absolute;
            bottom: 20px;
            right: 30px;
            font-size: 8rem;
            opacity: 0.1;
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }

            .fortune-result {
                font-size: 1.5rem;
            }

            .sections {
                flex-direction: column;
            }

            .character {
                display: none;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- 装饰元素 -->
        <div class="decoration decoration-1">🌸</div>
        <div class="decoration decoration-2">🌟</div>

        <div class="header">
            <h1>{{ name }}的今日运势</h1>
            <div class="date">{{ date }}</div>
        </div>

        <div class="fortune-result">
            <div class="fortune-icon">
               {% if fortune == "大吉" %}
                    <i class="fas fa-crown"></i>
                {% elif fortune == "中吉" %}
                    <i class="fas fa-sun"></i>
                {% elif fortune == "小吉" %}
                    <i class="fas fa-cloud-sun"></i>
                {% elif fortune == "末吉" %}
                    <i class="fas fa-seedling"></i>
                {% elif fortune == "吉带凶" %}
                    <i class="fas fa-cloud"></i>
                {% elif fortune == "中平" %}
                    <i class="fas fa-balance-scale"></i>
                {% elif fortune == "凶带吉" %}
                    <i class="fas fa-cloud-rain"></i>
                {% elif fortune == "小凶" %}
                    <i class="fas fa-umbrella"></i>
                {% elif fortune == "凶" %}
                    <i class="fas fa-cloud-showers-heavy"></i>
                {% elif fortune == "大凶" %}
                    <i class="fas fa-bolt"></i>
                {% else %}
                    <i class="fas fa-question"></i>
                {% endif %}
            </div>
            今日运势：<span style="font-size: 2.2rem;">{{ fortune }}</span>
        </div>

        {% if tips %}
        <div class="tips">
            {{ tips }}
        </div>
        {% endif %}

        <div class="sections">
            <div class="section good-section">
                <h2><i class="fas fa-thumbs-up"></i> 今日宜做</h2>

                {% for activity, desc in 宜.items() %}
                <div class="activity">
                    <div class="activity-icon">
                        {% set icons = ["😊", "👍", "✨", "💪", "🎯", "🍀", "❤️", "🏆"] %}
                        {{ icons | random }}
                    </div>
                    <div class="activity-content">
                        <div class="activity-title">{{ activity }}</div>
                        <div class="activity-desc">{{ desc }}</div>
                    </div>
                </div>
                {% endfor %}
            </div>

            <div class="section bad-section">
                <h2><i class="fas fa-thumbs-down"></i> 今日忌做</h2>

                {% for activity, desc in 忌.items() %}
                <div class="activity">
                    <div class="activity-icon">
                        {% set icons = ["😨", "⚠️", "🚫", "💥", "❌", "🙅", "⛔", "🤕"] %}
                        {{ icons | random }}
                    </div>
                    <div class="activity-content">
                        <div class="activity-title">{{ activity }}</div>
                        <div class="activity-desc">{{ desc }}</div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div class="footer">
            每日运势报告 · 祝您拥有美好的一天！
        </div>

        <div class="character">🐱</div>
    </div>
</body>
</html>
"""