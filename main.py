# 在这里编写代码
import requests
from bs4 import BeautifulSoup
import csv
import time

# 基础 URL
base_url = "https://www.shanghairanking.cn/rankings/bcur/202411"
# 请求头（防止反爬）
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def crawl_all_university_ranking():
    all_data = []
    page = 1

    while True:
        print(f"正在爬取第 {page} 页...")

        # 构造分页 URL
        url = f"{base_url}?page={page}"
        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"

        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.select("tbody tr")

        # 如果没有数据，说明已经到最后一页
        if not rows:
            print("未检测到数据，爬取结束")
            break

        for row in rows:
            cols = row.find_all("td")

            # 防止网页结构异常
            if len(cols) < 5:
                continue

            rank = cols[0].get_text(strip=True)
            university = cols[1].get_text(strip=True)
            province = cols[2].get_text(strip=True)
            university_type = cols[3].get_text(strip=True)
            score = cols[4].get_text(strip=True)

            all_data.append([
                rank, university, province, university_type, score
            ])

        page += 1
        time.sleep(1)  # 控制爬取速度，防止被封

    return all_data


def save_to_csv(data, filename="china_university_ranking_all.csv"):
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["排名", "学校名称", "省市", "类型", "总分"])
        writer.writerows(data)


if __name__ == "__main__":
    ranking_data = crawl_all_university_ranking()
    save_to_csv(ranking_data)
    print(f"爬取完成，共获取 {len(ranking_data)} 所高校排名数据")
